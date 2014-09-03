#install.packages(c("ggplot2","maps"))
require(ggplot2)
require(maps)
require(grid)

poker_users<-read.table("../geo/VideoDistributionModel/out/poker.out",col.names=c("lat","lon","rate","zone"),sep=",",comment.char="%")                    
mooc_users<-read.table("../geo/VideoDistributionModel/out/mooc.out",col.names=c("lat","lon","rate","zone"),sep=",",comment.char="%")
poker_users$type="Poker"
mooc_users$type="MOOC"
poker_users$norm_rate<-poker_users$rate/max(poker_users$rate)
mooc_users$norm_rate<-mooc_users$rate/max(mooc_users$rate)
users<-rbind(poker_users,mooc_users)
users<-users[sample(nrow(users)),]

#Get world map info
world_map <- map_data("world")

 
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
p <- ggplot() + coord_fixed(ylim=c(-60,80),xlim=c(-170,180)) +theme_opts
#Add map to base plot


base_world <- p + geom_polygon(data=world_map,
                aes(x=long, y=lat,group=group),alpha=I(0.1))

world <- base_world + scale_size_continuous(range = c(0.2,7))+
                            geom_point(data=users,
                                            aes(x=lon,
                                                y=lat,
                                                size=norm_rate,
                                                colour=type,
                                                shape=type),
                                         alpha=I(1.0)) 
                                         
world <- world +scale_colour_manual(values=c("#CC0000","#0000FF"))
world <- world +scale_shape_manual(values=c(0,1))
world <- world + guides(size="none", shape="none",colour=
    guide_legend((title="Activity"), override.aes= list(shape=c(0,1),size=c(3,3))))
#    override.aes = list(colour=c("black","black","black"), size=sizelist,
#    shape=shapelist)))
         
             

#pdf("out.pdf")
#print(map_with_jitter)
ggsave("graphs/demand_plot.pdf",width=6.0,height=2.05)
#dev.off()
