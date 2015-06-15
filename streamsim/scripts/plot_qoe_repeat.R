source ("scripts/readDataFiles.R")
require(ggplot2)
require(grid)
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 4) {
    cat("Requires dynamic1 dynamic2 no_users outputfile")
}
filename1<- args[1]
filename2<-args[2]
nousers<- as.numeric(args[3])
outfilename<- args[4]


dynamic1<-read_servers_file(filename1)
dynamic2<-read_servers_file(filename2)



dynamic1$type<-"d"
dynamic2$type<-"e"

combined<-rbind(dynamic1, dynamic2)
cat(combined$totdel,"\n")
cat(combined$totdelsd,"\n")
cat(combined$noservers,"\n")


col1<-"#990000"
col2<-"#00CC00"
col3<-"#0000FF"
allcols<-c(col1,col2,col3)
linetypes<-c(1,3)
shapetypes<-c(15,16)
typetypes<-c("d","e")
typenames<-c("Run1","Run2")
theme_opts <- theme_bw()



wid<-0.1
dodge<-c(wid*-0.5,0,wid*0.5)
minx<-min(dynamic1$noservers-wid*2)
maxx<-max(dynamic1$noservers+wid*2)
breaks<-as.numeric(levels(factor(dynamic1$noservers)))
g<-ggplot(combined,aes(x=noservers)) + theme_opts +
    scale_x_continuous(limits=c(minx-wid,maxx+wid),breaks=breaks)+
    expand_limits(y=0) +
    geom_errorbar(aes(x=noservers+dodge[1],ymin=mandel-2*mandelsd, ymax=mandel+2*mandelsd, colour="a",linetype=type), 
    width=wid) +
    geom_line(aes(x=noservers+dodge[1],y=mandel,colour="a",linetype=type))+
    geom_point(aes(x=noservers+dodge[1],y=mandel,colour="a",shape=type)) + 
    geom_errorbar(aes(x=noservers+dodge[2],ymin=unmandel-2*unmandelsd, ymax=unmandel+2*unmandelsd, colour="b",linetype=type), 
        width=wid) +
    geom_line(aes(x=noservers+dodge[2],y=unmandel,colour="b",linetype=type)) +
    geom_point(aes(x=noservers+dodge[2],y=unmandel,colour="b",shape=type)) +
    geom_errorbar(aes(x=noservers+dodge[3],ymin=totdel-2*totdelsd, ymax=totdel+2*totdelsd, colour="c",linetype=type), 
        width=wid) +
    geom_line(aes(x=noservers+dodge[3],y=totdel,colour="c",linetype=type)) +
    geom_point(aes(x=noservers+dodge[3],y=totdel,colour="c",shape=type)) +
    scale_colour_manual(breaks=c("a","b","c"),
        values=allcols, labels=c("managed","unmanaged","total"),
        guide = guide_legend(title = element_blank())) +
    scale_linetype_manual(name="combined",breaks=typetypes,
        values=linetypes, labels=typenames) +
    scale_shape_manual(name="combined",breaks=typetypes,
        values=shapetypes, labels=typenames) +
    guides(linetype= 
        guide_legend(title=element_blank())) +
    guides(shape= 
        guide_legend(title=element_blank())) +
    xlab("Number of cloud hosts/session") +
    ylab("Mean delay (secs)")
ggsave(outfilename,width=6.0,height=2.05)
