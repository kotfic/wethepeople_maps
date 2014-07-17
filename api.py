import requests
import json
import sys

def paged(window_size):    
    def paged_decorator(func):
        def paged_wrapper(*args, **kwargs):
            # Parse out the 'options' keyword argument if it exists,  or return {}
            # Then merge with with 'offset' : 0,  'limit' : window_size and pack it back up into
            # a dict.  This will set defaults for offset and limit unless they have already 
            # been set in kwargs['options'] 
            options = dict({'offset' : 0, 'limit' : window_size}.items() + kwargs.get('options', {}).items())

            meta, ret = func(*args, options=options)
            if ret:
                while len(ret) < meta['count']:
                    options['offset'] = options['offset'] + options['limit']
                    meta, items = func(*args, options=options)
                    if items:
                        ret += items
                    else:
                        break
            
            return ret
 
        return paged_wrapper
    return paged_decorator
             
 


class PetitionAPI:
    base_url = "https://api.whitehouse.gov/v1/"


    def __init__(self, response_type="json"):
        self.response_type = response_type
        self.headers = {}

    # Functions for communicating with the API and processing responses

    def _api_get(self, resource, options = {} ):
        """Makes the actual call out to the petition api endpoint and returns a python object
        from the request.text using json.loads"""
        # add "options" key/values as get params 
        url = self.base_url + resource + "." + self.response_type
        if len(options.items()):
            url = url + "?" + '&'.join([str(key) + "=" + str(value) for key,value in options.items()])

        r = requests.get( url, headers=self.headers )

        print("{}: {}".format(r.status_code, url))
        sys.stdout.flush()

        if r.status_code != 200:
            print("{}".headers() )
            return False

        return json.loads(r.text)
        

    def api_get(self, url, options = {} ):
        """Calls _api_get() and then does some response processing to normalize the responses from the whitehouse API"""
        results = self._api_get(url, options)
        
        try:
            metadata = {}
            for key, val in results['metadata'].items():
                if type(val) == dict:
                    metadata = dict(metadata.items() + val.items())
                else:
                    metadata = dict(metadata.items() + [(key, val)])
            
            if 'noresults' in results.keys():
                metadata['noresults'] = results['noresults']
            else:
                metadata['noresults'] = 0

            return (metadata, results['results'])

        except:
            return (False, False)

    # Base functions for getting petitions and signatures
            
    @paged(1000)
    def get_petition_collection(self, options=None):
        """Returns a collection of petitions, Note:  options MUST be passed in as a keyword argument to work"""
        metadata, collection = self.api_get("petitions", options)
        return (metadata, collection)

    @paged(1000)
    def get_signature_collection(self, petition_id, options=None):
        """Returns a collection of petition signatures, Note:  options MUST be passed in as a keyword argument to work"""
        metadata, collection = self.api_get("petitions/%s/signatures" % petition_id, options)
        # Signatures coming back from the API do not include their petition_id
        try:
            for sig in collection:
                sig['petition_id'] = petition_id
        except TypeError:
            pass

        return (metadata, collection)
    

    def get_petition(self, id):
        """Return a specific petition by its id"""
        metadata, petition = self.api_get("petitions/%s" % id)
        try:            
            return petition[0]
        except:
            return False


    # Functions for doing higher level petition/signature filtering

    def get_petitions_after(self, timestamp):
        pass
        
    @paged(1000)
    def get_petitions_before(self, timestamp):
        metadata, collection = self.api_get("petitions", options={"createdBefore" : timestamp})
        return (metadata, collection)

        return self.get_petition_collection(options={"createdBefore" : timestamp})

    def get_petitions_between(self, start, end):
        pass

    def get_signatures_after(self, petition_id, timestamp):
        pass
        
    def get_signatures_before(self, petition_id, timestamp):
        pass

    def get_signatures_between(self, petition_id, start, end):
        pass

    
    def with_petition_collection(self, func, options=None):
        pass

    def with_petition_signatures(self, petition_id, func, options=None):
        pass




api = PetitionAPI()

if __name__ == "__main__":
    sigs = api.get_signature_collection("530b81dd7043017077000009")
    with open("sigs2.json", "w") as h:
        h.write(json.dumps(sigs))
    
