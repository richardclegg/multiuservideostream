source ("scripts/readDataFiles.R")
require(ggplot2)
require(grid)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 4) {
    cat("Requires random static dynamics no_users outputfile")
}
filename1<- args[1]
filename2<-args[2]
filename3<-args[3]
outfilename<- args[4]

random<-read_servers_file(filename1)
static<-read_servers_file(filename2)
dynamic<-read_servers_file(filename3)

col1<-"#990000"
col2<-"#00CC00"
col3<-"#0000FF"
allcols<-c(col1,col2,col3)

theme_opts <- theme_bw()


wid<-0.1
dodge<-c(wid*-1,0,wid)
minx<-min(random$noservers-wid*2)
maxx<-max(random$noservers+wid*2)
breaks<-as.numeric(levels(factor(random$noservers)))
g<-ggplot(random,aes(x=noservers)) + theme_opts +
    scale_x_continuous(limits=c(minx-wid,maxx+wid),breaks=breaks)+
    expand_limits(y=0) +
    geom_errorbar(aes(x=noservers+dodge[1],ymin=percman-2*percmansd, ymax=percman+2*percmansd, colour="a"), 
    width=wid) +
    geom_line(aes(x=noservers+dodge[1],y=percman,colour="a"))+
    geom_point(aes(x=noservers+dodge[1],y=percman,colour="a")) + 
    geom_errorbar(data=static, aes(x=noservers+dodge[2],ymin=percman-2*percmansd, ymax=percman+2*percmansd, colour="b"), 
        width=wid) +
    geom_line(data=static, aes(x=noservers+dodge[2],y=percman,colour="b")) +
    geom_point(data=static, aes(x=noservers+dodge[2],y=percman,colour="b")) +
    geom_errorbar(data=dynamic, aes(x=noservers+dodge[3],ymin=percman-2*percmansd, ymax=percman+2*percmansd, colour="c"), 
        width=wid) +
    geom_line(data=dynamic,aes(x=noservers+dodge[3],y=percman,colour="c")) +
    geom_point(data=dynamic,aes(x=noservers+dodge[3],y=percman,colour="c")) +
    scale_colour_manual(breaks=c("a","b","c"),
        values=allcols, labels=c("random","static","dynamic"),
        guide = guide_legend(title = element_blank())) + 
    xlab("Number of servers") +
    ylab("% managed net")
ggsave(outfilename,width=6.0,height=2.05)
