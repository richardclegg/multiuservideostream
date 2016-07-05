source ("scripts/readDataFiles.R")
require(ggplot2)
require(grid)
varnames=c("noservers","day","daysd","incost","incostsd",
    "betweencost","betweencostsd","outcost","outcostsd",
    "cpucost","cpucostsd", "totcost","totcostsd",
    "day2","sdday2","percman","percmansd", 
    "mandel","mandelsd","mandelsd2","mandelsd2sd",
    "totdel","totdelsd","totdelsd2","totdelsd2sd",
    "mq1","mq1sd","mq2","mq2sd","mq3","mq3sd","mq4","mq4sd","mq5","mq5sd",
    "uq1","uq1sd","uq2","uq2sd","uq3","uq3sd","uq4","uq4sd","uq5","uq5sd",
    "day3","sdday3", 
    "meansessno","meansessnosd",
    "sdsessno","sdsessnosd",
    "maxsessno","maxsessnosd",
    "meanusers","meanuserssd",
    "sdusers","sduserssd", 
    "maxusers","maxuserssd")
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 5) {
    cat("Requires random static dynamics no_users outputfile")
}
filename1<- args[1]
filename2<-args[2]
filename3<-args[3]
nousers<- as.numeric(args[4])
outfilename<- args[5]

random<-read_servers_file(filename1)
static<-read_servers_file(filename2)
dynamic<-read_servers_file(filename3)

#cat(random$unmandel,"\n")
#cat(static$unmandel,"\n")
#cat(dynamic$unmandel,"\n")
#cat(dynamic$unmandel,"\n")

random$type<-"d"
static$type<-"e"
dynamic$type<-"f"
combined<-rbind(random,static,dynamic)

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
    geom_errorbar(aes(x=noservers+dodge[1],ymin=mandel-2*mandelsd2, ymax=mandel+2*mandelsd2, colour="a"), 
        width=wid) +
    geom_line(aes(x=noservers+dodge[1],y=mandel,colour="a",linetype=type))+
    geom_point(aes(x=noservers+dodge[1],y=mandel,colour="a",shape=type)) + 
    geom_errorbar(aes(x=noservers+dodge[2],ymin=unmandel-2*unmandelsd2, ymax=unmandel+2*unmandelsd2, colour="b"), 
        width=wid) +
    geom_line(aes(x=noservers+dodge[2],y=unmandel,colour="b",linetype=type)) +
    geom_point(aes(x=noservers+dodge[2],y=unmandel,colour="b",shape=type)) +
    geom_errorbar(aes(x=noservers+dodge[3],ymin=totdel-2*totdelsd2, ymax=totdel+2*totdelsd2, colour="c"), 
        width=wid) +
    geom_line(aes(x=noservers+dodge[3],y=totdel,colour="c",linetype=type)) +
    geom_point(aes(x=noservers+dodge[3],y=totdel,colour="c",shape=type)) +
    scale_colour_manual(breaks=c("a","b","c"),
        values=allcols, labels=c("managed","unmanaged","total"),
        guide = guide_legend(title = element_blank())) +
    scale_linetype_manual(name="combined",breaks=c("d","e","f"),
        values=linetypes, labels=c("random","static","dynamic")) +
    scale_shape_manual(name="combined",breaks=c("d","e","f"),
        values=shapetypes, labels=c("random","static","dynamic")) +
    guides(linetype= 
        guide_legend(title=element_blank())) +
    guides(shape= 
        guide_legend(title=element_blank())) +
    xlab("Number of cloud hosts/session") +
    ylab("Mean delay (secs)")
ggsave(outfilename,width=6.0,height=2.05)
