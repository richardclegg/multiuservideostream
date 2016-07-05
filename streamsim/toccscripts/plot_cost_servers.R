source ("scripts/readDataFiles.R")
require(ggplot2)
require(grid)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 6) {
    cat("Requires random static dynamics no_users outputfile")
    exit()
}
filename1<- args[1]
filename2<-args[2]
filename3<-args[3]
nousers<- as.numeric(args[4])
dur<-as.numeric(args[5])
outfilename<- args[6]

random<-read_servers_file(filename1)
static<-read_servers_file(filename2)
dynamic<-read_servers_file(filename3)



wid<-0.1
dodge<-c(-wid/3,0,wid/3.0)

col1<-"#990000"
col2<-"#00CC00"
col3<-"#0000FF"
allcols<-c(col1,col2,col3)
linetypes<-c("dashed","solid","dotted")
shapetypes<-c(16,17,15)


minx<-min(random$noservers-wid*2)
maxx<-max(random$noservers+wid*2)

theme_opts <- theme_bw()
#list(theme(
#                        axis.text.x= element_text(colour="black"),
#                        axis.text.y= element_text(colour="black"),
#                        panel.grid.minor = element_line(color="#AAAAAA"),
#                        panel.background = element_blank(),
#                        plot.margin = unit(c(0,0,0,0),"mm")))


random$type<-"d"
static$type<-"e"
dynamic$type<-"f"
random$dodge2<- -wid
static$dodge2<- 0
dynamic$dodge2<- wid
combined<-rbind(random,static,dynamic)
combined$utotcost<-combined$totcost/(nousers*dur)
combined$utotcostsd<-combined$totcostsd/(nousers*dur)
combined$ubetweencost<-combined$betweencost/(nousers*dur)
combined$ubetweencostsd<-combined$betweencostsd/(nousers*dur)
breaks<-as.numeric(levels(factor(random$noservers)))
    
g<-ggplot(combined,aes(x=noservers)) + theme_opts +
    scale_x_continuous(limits=c(minx-wid,maxx+wid),breaks=breaks)+
        scale_colour_manual(name="combined",breaks=c("d","e","f"),
        values=allcols, labels=c("random","static","dynamic"),
        guide = guide_legend(title = element_blank())) +
    scale_shape_manual(name="combined",breaks=c("d","e","f"),
        values=shapetypes, labels=c("random","static","dynamic")) +    
    scale_linetype_manual(breaks=c("a","b"),
        values=linetypes, labels=c("managed","total")) +
    expand_limits(y=0) +
    geom_errorbar(aes(x=noservers+dodge[1]+dodge2,ymin=ubetweencost-2*ubetweencostsd, ymax=ubetweencost+2*ubetweencostsd, colour=type), width=wid) +
    geom_line(aes(x=noservers+dodge[1]+dodge2,y=ubetweencost,colour=type,linetype="a"))+
    geom_point(aes(x=noservers+dodge[1]+dodge2,y=ubetweencost,colour=type,shape=type),size=2.5) + 
    geom_errorbar(aes(x=noservers+dodge[2]+dodge2,ymin=utotcost-2*utotcostsd, ymax=utotcost+2*utotcostsd, colour=type), width=wid) +
    geom_line(aes(x=noservers+dodge[2]+dodge2,y=utotcost,colour=type,linetype="b")) +
    geom_point(aes(x=noservers+dodge[2]+dodge2,y=utotcost,colour=type,shape=type),size=2.5) +
    guides(linetype= 
        guide_legend(title=element_blank())) +
    guides(shape= 
        guide_legend(title=element_blank())) +        
    xlab("Number of cloud hosts/session") +
    ylab("Mean cost per user hour ($)")
ggsave(outfilename,width=6.0,height=4.0)
