library(MASS)
library(mapdata)
library(animation)
if(! exists("dat")){
    bbox <-  dat$lat < 50.0 & dat$lat > 25.0 & dat$lon > -130.0 & dat$lon < -60.0
    interval <- 3600

    dat <- read.csv("data/lat_lon_530b81dd7043017077000009.csv")

    # There is a better way to do this I am sure
    for (i in 1:ceiling((max(dat$created) - min(dat$created)) / interval)){
        dat$intervals[dat$created <=  min(dat$created) + (interval * i) &
                          dat$created >  min(dat$created) + (interval * (i - 1))] <- min(dat$created) + (interval * i)
    }
}


# TODO
# Show first 150 signatures in different color

# set makeGIF up to show each of 150 original signatures
#   Then display hourlies 

# Show signature frequency vs time over duration of the
#   petition with line showing when we're located


plotMapAndHourly <- function(i){
    layout(matrix(c(1, rep(2, 2))))
    par(mar=c(5,4,4,1) + 0.1)

    hourlyCounts <- aggregate(dat$intervals, list(ts = dat$intervals), length)
    plot(hourlyCounts$ts, hourlyCounts$x, cex=0.4, xaxt="n", xlab="Time", ylab="Signatures")

    title("GIS time laps of Petition\n'Declare Major League Baseball Opening Day a national holiday.'")

    
    # select 6 ticks plus the first date
    tickSelector <- !(1:length(hourlyCounts$ts) %% (length(hourlyCounts$ts) / 6))
    tickSelector[1] <- TRUE

    axis(1, at=hourlyCounts$ts[tickSelector],
         labels=format(as.POSIXlt(hourlyCounts$ts[tickSelector], origin="1970-01-01"), "%b-%d"))

    
    
    abline(v=min(dat$created) + (interval * i)
         , lwd=2, col = rgb(0, 0, 255, 255, maxColorValue=255))


    filter <- bbox & (dat$created <= min(dat$created) + (interval * i))

    par(mar=c(5,4,4,2) + 0.1)

    map("usa", interior=FALSE, resolution=0)
    map("state", boundary = FALSE, col="grey", add=TRUE)

    title(sprintf("%s Signatures as of: %s",
                  length(which(filter)),
                  as.POSIXlt(min(dat$created) + interval * i,
                             origin = "1970-01-01")))
        

    points(dat$lon[filter], dat$lat[filter], col=rgb(0,0,255,50, maxColorValue=255), cex=0.1)

    if (length(which(filter)) > 2000){
        contour(kde2d(dat$lon[filter], dat$lat[filter]), add=T)
    }
}


for (i in 1:length(unique(dat$intervals))) {
# for (i in 757:757) {
    print(sprintf("Generating img/img_%s.png", i))
    png(sprintf("img/img_%04d.png", i), width=1000, height=1000, res=200)
    plotMapAndHourly(i)
    dev.off()
}

