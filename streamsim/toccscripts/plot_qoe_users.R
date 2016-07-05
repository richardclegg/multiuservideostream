require(ggplot2)
require(grid)
source("scripts/readDataFiles.R")
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
    cat("Requires input and output filename as argument")
}
filename1<- args[1]
filename2<-args[2]
outfilename<- args[3]


plotdat<-read_users_file(filename1)
plotdat2<-read_users_file(filename2)

col1<-"#990000"
col2<-"#00CC00"
col3<-"#0000FF"
col4<-"#000000"
allcols<-c(col1,col2,col3,col4)

theme_opts <- theme_bw()



wid<-100
dodge<-c(wid*-1.5,wid*-.5,wid*.5,wid*1.5)
minx<-min(plotdat$nousers-wid*2)
maxx<-max(plotdat$nousers+wid*2)
breaks<-as.numeric(levels(factor(plotdat$nousers)))
g<-ggplot(plotdat,aes(x=nousers)) + theme_opts +
    scale_x_continuous(limits=c(minx-wid,maxx+wid),breaks=breaks)+
    expand_limits(y=0) +
    geom_errorbar(aes(x=nousers++dodge[1],ymin=mandel-2*mandelsd, ymax=mandel+2*mandelsd, colour="a"), 
    width=wid) +
    geom_line( aes(x=nousers+dodge[1],y=mandel,colour="a"))+
    geom_point(aes(x=nousers+dodge[1],y=mandel,colour="a")) + 
    geom_errorbar(aes(x=nousers+dodge[2],ymin=unmandel-2*unmandelsd, ymax=unmandel+2*unmandelsd, colour="b"), 
        width=wid) +
    geom_line(aes(x=nousers+dodge[2],y=unmandel,colour="b")) +
    geom_point(aes(x=nousers+dodge[2],y=unmandel,colour="b")) +
    geom_errorbar(aes(x=nousers+dodge[3],ymin=totdel-2*totdelsd, ymax=totdel+2*totdelsd, colour="c"), 
        width=wid) +
    geom_line(aes(x=nousers+dodge[3],y=totdel,colour="c")) +
    geom_point(aes(x=nousers+dodge[3],y=totdel,colour="c")) +
    geom_errorbar(data=plotdat2,aes(x=nousers+dodge[4],ymin=unmandel-2*unmandelsd, ymax=unmandel+2*unmandelsd, colour="d"), 
        width=wid) +
    geom_line(data=plotdat2,aes(x=nousers+dodge[4],y=unmandel,colour="d")) +
    geom_point(data=plotdat2,aes(x=nousers+dodge[4],y=unmandel,colour="d")) +
    scale_colour_manual(breaks=c("a","b","c","d"),
        values=allcols, labels=c("managed","unmanaged","total","potato"),
        guide = guide_legend(title = element_blank())) + 
    xlab("Number of users") +
    ylab("Delay (s)")
ggsave(outfilename,width=6.0,height=2.05)
