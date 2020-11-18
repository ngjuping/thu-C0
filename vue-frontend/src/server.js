import { Server, Model,Response  } from 'miragejs'

export function makeServer({ environment = "development" } = {}) {


let server = new Server({
  environment,

    models: {
      user: Model,
      notice: Model,
      venue: Model,
    },
    
  seeds(server) {
      //create a default user
      server.create("user", { user_id:'admin',password:'123456',name:"Admin" });

      //create 4 notices
      server.create("notice", { title:"正式启动",content:"马上体验" });
      server.create("notice", { title:"Hello World",content:"Lorem Ipsum" });
      server.create("notice", { title:"主页，登陆，注册页",content:"采用bootstrap框架" });
      server.create("notice", { title:"Hello World",content:"Lorem Ipsum" });

      //create info for EACH venue
      server.create("venue", { 
        name:"新林院", 
        description:"鸟语花香的环境，和蔼可亲的工作人员，舒适的场地——你一定会爱上这里。", 
        img:"https://miro.medium.com/max/1140/0*16bH8WYK3fOtu-kJ.jpg", 
        notice:[{ title:"闭馆通知",content:"请注意，11月15日闭馆" },{ title:"场地折扣10%",content:"即日起至12月1日" }],
        review:{stars:4,content:"场地不错，服务还行，稍微贵了些",publish_date:"2013-03-01T00:00:00+01:00"},
        courts:[
          {id:0,type:0,status:[{start:"0900",end:"1000",code:0},{start:"1000",end:"1100",code:1},{start:"1100",end:"1200",code:0}]},
          {id:1,type:1,status:[{start:"0900",end:"1000",code:0},{start:"1000",end:"1100",code:1},{start:"1100",end:"1200",code:1}]},
        ]
      });
      
      server.create("venue", { 
        name:"活动中心" , 
        description:"Normal venue", 
        img:"https://blog.playo.co/wp-content/uploads/2018/09/5b3f1476cb29c_badminton1.jpg",
        notice:[{ title:"闭馆通知",content:"小心了，11月15日闭馆" },{ title:"场地折扣5%",content:"只限马杯赛事场地" }],
        review:{stars:5,content:"还行",publish_date:"2017-03-01T00:00:00+01:00"},
        courts:[
          {id:0,type:0,status:[{start:"0900",end:"1000",code:0},{start:"1000",end:"1000",code:1}]},
          {id:1,type:1,status:[{start:"0900",end:"1000",code:0},{start:"1000",end:"1000",code:1}]},
        ]
    });
      
    },


  routes() {

    this.namespace = "api/v1";

    //access data: res.data.user_id
    this.post("/login", (schema,request) => {
        let attrs = JSON.parse(request.requestBody);

        let selected_user = schema.users.findBy({user_id:attrs.user_id});

        if(selected_user.password == attrs.password){
          return {"message":"ok", user_id:attrs.user_id};
        }
        else{
          return {"message":"not ok"};
        }

    })

    //access data: res.data.user_id
    this.post("/signup", (schema,request) => {
        let attrs = JSON.parse(request.requestBody);
        console.log(attrs);
        let existed_user = schema.users.findBy({user_id:attrs.user_id});

        if(existed_user)
        {
          return new Response(400, {}, { message: "not ok" });
        }
        else
        {
          schema.users.create({
            user_id:attrs.user_id,
            password:attrs.password,
            name:attrs.name
          });
    
          return {"message":"ok",user_id:attrs.user_id};
        }
    });

    //access data: this.notices = res.data.notices;
    this.get("/main/notice", (schema) => {
      
      return schema.notices.all();
    
    });

    //access data: this.venues = res.data.venues;
    this.get("/venues/list", (schema) => {
      
      return schema.venues.all();
    
    });

    //access data: this.currentvenue = res.data.venue;
    this.get("/venues/:id")

    this.get("/booking",(schema,request)=>{
      
      let selected_venue = schema.venues.findBy({id:request.queryParams.id});
      
      return {venue_name:selected_venue.attrs.name,courts:selected_venue.attrs.courts};
    })
  }
  
})
  
  return server;
}