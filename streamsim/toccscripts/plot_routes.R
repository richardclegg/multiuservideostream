#install.packages(c("ggplot2","maps"))
require(ggplot2)
require(maps)
require(grid)
require(geosphere)
require(plyr)
 
varnames<-c("lat1","lon1","lat2","lon2","bw","type") 
args <- commandArgs(trailingOnly = TRUE)
filename1<-args[1]
filename2<-args[2]
routes<-read.table(filename1,col.names=varnames)
routes$l1<-cbind(routes[,2], routes[,1])
routes$l2<-cbind(routes[,4], routes[,3])
rts<-gcIntermediate(routes$l1,routes$l2, n=50, breakAtDateLine=TRUE, addStartEnd=TRUE, sp=TRUE)
#Get world map info
fortify.SpatialLinesDataFrame <- function(model, data, ...) {
  ldply(model@lines, fortify)
}
rts<-fortify.SpatialLinesDataFrame(rts)
world_map <- map_data("world")
routes$id <-as.character(c(1:nrow(routes)))
gcircles <- merge(rts, routes, all.x=T, by="id")
gcircles$t <-factor(gcircles$type)
# create a blank ggplot theme
theme_opts <- list(theme(panel.grid.minor = element_blank(),
                        panel.grid.major = element_blank(),
                        panel.background = element_blank(),
                        plot.margin = unit(c(0,0,0,0),"mm"),
                        panel.border = element_blank(),
                        axis.line = element_blank(),
                        axis.text.x = element_blank(),
                        axis.text.y = element_blank(),
                        axis.ticks = element_blank(),
                        axis.title.x = element_blank(),
                        axis.title.y = element_blank(),
                        plot.title = element_text(size=22)))
                        
#Creat a base plot
p <- ggplot()  + coord_fixed(ylim=c(-60,80),xlim=c(-170,180)) +
    theme_opts + geom_polygon(data=world_map,
            aes(x=long, y=lat,group=group),alpha=I(0.2))+ 
             geom_line(data=gcircles,
                aes(long,lat,group=group,colour=t,size=(bw*8))) +
         scale_colour_manual(values=c("#FF0000","#000000"),
            labels=c("Unmanaged","Managed"),
         guide = guide_legend(title = "Connection")) +
         scale_size_continuous(range = c(0, 2.0), 
         guide = guide_legend(title = "bandwidth(Mb/s)"))
             

#pdf("out.pdf")
#print(map_with_jitter)
ggsave(filename2,width=6.0,height=2.05)
#dev.off()
