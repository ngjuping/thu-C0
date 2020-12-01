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
      //create 2 default user
      server.create("user", { api_id:'ordinary',pwd:'111111',name:"ordinary",status:0,privilege:0});//普通用户
      server.create("user", { api_id:'admin',pwd:'123456',name:"Admin",status:0,privilege:1});//管理员

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
          {
            id:1,
            type:1,
            status:[
              {start:"2020-11-26T10:00:00+01:00",end:"2020-11-26T11:00:00+01:00",code:1},
              {start:"2020-11-26T11:00:00+01:00",end:"2020-11-26T12:00:00+01:00",code:1},
              {start:"2020-11-26T12:00:00+01:00",end:"2020-11-26T13:00:00+01:00",code:1}]
          }
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

        let selected_user = schema.users.findBy({api_id:attrs.api_id});


        try{
          if(selected_user.pwd == attrs.pwd){

            selected_user.update({ status: 1 });
            
            return {message:"ok", user_info:{ user_id:parseInt(selected_user.id),name:selected_user.name,privilege:selected_user.privilege }};
          }
          else{
            return new Response(400, {}, {message:"User doesn't exist"});
          }
        }
        catch(e){
          return new Response(400, {}, {message:"User doesn't exist"});
        }


    })

    this.post("/logout", (schema,request) => {

        let attrs = JSON.parse(request.requestBody);
        
        let selected_user = schema.users.findBy({id:attrs.user_id});

        selected_user.update({ status: 0 });

        return {message:"ok"};
    })


    this.post("/signup", (schema,request) => {
        let attrs = JSON.parse(request.requestBody);
        let existed_user = schema.users.findBy({api_id:attrs.api_id});

        if(existed_user)
        {
          return new Response(400, {}, { message: "wrong id or password" });
        }
        else
        {
          let new_user = schema.users.create({
            api_id:attrs.api_id,
            pwd:attrs.pwd,
            name:attrs.name
          });
    
          return {message:"ok",user_id:parseInt(new_user.id)};
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
            end:"2021-11-01T00:00:00+01:00"
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
          status:2
          },
        ]
        };
    });
    let all_notices = [{
      title: "title 1",
      content: "content 1"
    },
    {
      title: "title 2",
      content: "content 2"
    },
    {
      title: "title 3",
      content: "content 3"
    },
    {
      title: "title 4",
      content: "content 4"
    },
    {
      title: "title 5",
      content: "content 5"
    },
    {
      title: "title 6",
      content: "content 6"
    },
    {
      title: "title 7",
      content: "content 7"
    },
    {
      title: "title 8",
      content: "content 8"
    },
    {
      title: "title 9",
      content: "content 9"
    },
    {
      title: "title 10",
      content: "content 10"
    }];

    this.get('/notices',(schema,request)=>{
      let requested_page = request.queryParams.page;
      if(requested_page < 1 || (requested_page-1)*5 > all_notices.length){
        return new Response(422, {}, { message: "页面不存在" });
      }
      
      return {
        message:"ok",
        total:all_notices.length,
        notices: all_notices.slice((requested_page-1)*5,(requested_page)*5)
      }
    })

    
  }
  
})
  
  return server;
}