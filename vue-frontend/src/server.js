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
      server.create("user", { user_id:'admin',pwd:'123456',name:"Admin",status:0 });

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
        notices:[{ title:"闭馆通知",content:"请注意，11月15日闭馆" },{ title:"场地折扣10%",content:"即日起至12月1日" }],
        review:{stars:4,content:"场地不错，服务还行，稍微贵了些",publish_date:"2013-03-01T00:00:00+01:00"},
        courts:[
          {id:1,type:1,status:[{start:"0900",end:"1000",code:0},{start:"1000",end:"1100",code:1},{start:"1100",end:"1200",code:0},
          {start:"1200",end:"1300",code:0},{start:"1300",end:"1400",code:0},{start:"1400",end:"1500",code:0},{start:"1500",end:"1600",code:0},
          {start:"1600",end:"1700",code:1},{start:"1700",end:"1800",code:1},{start:"1800",end:"1900",code:0},{start:"1900",end:"2000",code:0}]},
          
          {id:2,type:2,status:[{start:"0900",end:"1000",code:0},{start:"1000",end:"1100",code:1},{start:"1100",end:"1200",code:1}]},
          {id:3,type:3,status:[{start:"0900",end:"1000",code:1},{start:"1000",end:"1100",code:1},{start:"1100",end:"1200",code:1},{start:"1200",end:"1300",code:1}
          ,{start:"1300",end:"1400",code:1},{start:"1400",end:"1500",code:0},{start:"1500",end:"1600",code:0}]},
        ]
      });
      
      server.create("venue", { 
        name:"活动中心" , 
        description:"Normal venue", 
        img:"https://blog.playo.co/wp-content/uploads/2018/09/5b3f1476cb29c_badminton1.jpg",
        notices:[{ title:"闭馆通知",content:"小心了，11月15日闭馆" },{ title:"场地折扣5%",content:"只限马杯赛事场地" }],
        review:{stars:5,content:"还行",publish_date:"2013-03-01T00:00:00+01:00"},
        courts:[
          {id:4,type:1,status:[{start:"0900",end:"1000",code:0},{start:"1000",end:"1000",code:1}]},
          {id:5,type:2,status:[{start:"0900",end:"1000",code:0},{start:"1000",end:"1000",code:1}]},
        ]
    });
      
    },


  routes() {

    this.namespace = "api";

    this.post("/login", (schema,request) => {
        let attrs = JSON.parse(request.requestBody);

        let selected_user = schema.users.findBy({user_id:attrs.user_id});


        try{
          if(selected_user.pwd == attrs.pwd){

            selected_user.update({ status: 1 });
            
            return {message:"ok", user_info:{ user_id:attrs.user_id,name:selected_user.name }};
          }
        }
        catch(e){
          return new Response(400, {}, {message:"User doesn't exist"});
        }


    })

    this.post("/logout", (schema,request) => {

        let attrs = JSON.parse(request.requestBody);

        console.log(attrs);
        
        let selected_user = schema.users.findBy({user_id:attrs.user_id});

        console.log(selected_user);

        selected_user.update({ status: 0 });

        return {message:"ok"};
    })


    this.post("/signup", (schema,request) => {
        let attrs = JSON.parse(request.requestBody);
        let existed_user = schema.users.findBy({user_id:attrs.user_id});

        if(existed_user)
        {
          return new Response(400, {}, { message: "wrong id or password" });
        }
        else
        {
          schema.users.create({
            user_id:attrs.user_id,
            pwd:attrs.pwd,
            name:attrs.name
          });
    
          return {message:"ok",user_id:attrs.id};
        }
    });

    //access data: this.notices = res.data.notices;
    this.get("/main/notices", (schema) => {
      
      return schema.notices.all();
    
    });

    //access data: this.venues = res.data.venues;
    this.get("/main/venues/list", (schema) => {
      
      return schema.venues.all();
    
    });

    //access data: this.currentvenue = res.data.venue;
    this.get("/main/venues",(schema,request)=>{
      let selected_venue = schema.venues.findBy({id:request.queryParams.id});
      return {message:"ok",venue_info:selected_venue}
    })

    this.get("/booking",(schema,request)=>{
      
      let selected_venue = schema.venues.findBy({id:request.queryParams.id});
      
      return {venue_name:selected_venue.attrs.name,courts:selected_venue.attrs.courts};
    })

    this.post("/book", (schema,request) => {
      let attrs = JSON.parse(request.requestBody);
      let courtisbooked = false;
      if(attrs.start == "24-11-2020T10:00:00+01:00")
        courtisbooked = true;
      if(courtisbooked)
      {
        return new Response(422, {}, { message: "场地已被预定" });
      }
      return {message:"ok"};
      
    });

    this.get('/manage/courts',(schema,request) => {
      console.log(request.queryParams.user_id);
      return {
        message:"ok",
        courts:[
        {
          id:1,
          type:1,
          details:{
            name: "新林院羽球场01",
            start:"2020-10-01T00:00:00+01:00",
            end:"2020-11-01T00:00:00+01:00"
            },
          status:1
        },
        {
          id:2,
          type:2,
          details:{
            name: "活动中心网球场03",
            start:"2020-03-01T00:00:00+01:00",
            end:"2020-03-01T00:00:00+01:00"
            },
          status:1
          },
        ]
        };
    });

    
  }
  
})
  
  return server;
}