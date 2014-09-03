require(ggplot2)
require(grid)
source ("scripts/readDataFiles.R")
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 4) {
    cat("Requires file no_users duration outputfile")
    return
}
filename1<- args[1]
nousers<- as.numeric(args[2])
dur<-as.numeric(args[3])
outfilename<- args[4]


random<-read_servers_file(filename1)
random$utotcost<-random$totcost/(nousers*dur)
random$utotcostsd<-random$totcostsd/(nousers*dur)


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
    geom_errorbar(aes(x=noservers+dodge[1],ymin=utotcost-2*utotcostsd, ymax=utotcost+2*utotcostsd), 
    width=wid) +
    geom_line(aes(x=noservers+dodge[1],y=utotcost))+
    geom_point(aes(x=noservers+dodge[1],y=utotcost)) +
    xlab("Number of servers") +
    ylab("Mean cost per user hour $")
ggsave(outfilename,width=6.0,height=2.05)
