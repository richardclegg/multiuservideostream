source ("scripts/readDataFiles.R")
require(ggplot2)
require(grid)
source("scripts/readDataFiles.R")
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
    cat("Requires file no_users outputfile")
    return
}
filename1<- args[1]
nousers<- as.numeric(args[2])
outfilename<- args[3]

random<-read_servers_file(filename1)

#cat(random$unmandel,"\n")
#cat(static$unmandel,"\n")
#cat(dynamic$unmandel,"\n")
#cat(dynamic$unmandel,"\n")

random$type<-"d"
combined<-random

col1<-"#990000"
col2<-"#00CC00"
col3<-"#0000FF"
allcols<-c(col1,col2,col3)
linetypes<-c(1,3,4)
shapetypes<-c(16,17,15)
theme_opts <- theme_bw()


wid<-0.1
dodge<-c(wid*-1,0,wid)
minx<-min(random$noservers-wid*2)
maxx<-max(random$noservers+wid*2)
breaks<-as.numeric(levels(factor(random$noservers)))
g<-ggplot(combined,aes(x=noservers)) + theme_opts +
    scale_x_continuous(limits=c(minx-wid,maxx+wid),breaks=breaks)+
    expand_limits(y=0) +
    geom_errorbar(aes(x=noservers+dodge[1],ymin=mandel-2*mandelsd, ymax=mandel+2*mandelsd, colour="a"), 
        width=wid) +
    geom_line(aes(x=noservers+dodge[1],y=mandel,colour="a",linetype=type))+
    geom_point(aes(x=noservers+dodge[1],y=mandel,colour="a",shape=type)) + 
    geom_errorbar(aes(x=noservers+dodge[2],ymin=unmandel-2*unmandelsd, ymax=unmandel+2*unmandelsd, colour="b"), 
        width=wid) +
    geom_line(aes(x=noservers+dodge[2],y=unmandel,colour="b",linetype=type)) +
    geom_point(aes(x=noservers+dodge[2],y=unmandel,colour="b",shape=type)) +
    geom_errorbar(aes(x=noservers+dodge[3],ymin=totdel-2*totdelsd, ymax=totdel+2*totdelsd, colour="c"), 
        width=wid) +
    geom_line(aes(x=noservers+dodge[3],y=totdel,colour="c",linetype=type)) +
    geom_point(aes(x=noservers+dodge[3],y=totdel,colour="c",shape=type)) +
    scale_colour_manual(breaks=c("a","b","c"),
        values=allcols, labels=c("managed","unmanaged","total"),
        guide = guide_legend(title = element_blank())) +
    xlab("Number of cloud hosts/session") +
    ylab("Mean delay (secs)")
ggsave(outfilename,width=6.0,height=2.05)
