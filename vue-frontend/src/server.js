import { Server, Model,Response  } from 'miragejs'

export function makeServer({ environment = "development" } = {}) {


let server = new Server({
  environment,

    models: {
      user: Model,
      notice: Model,
      venue: Model
    },
    
  seeds(server) {
      server.create("user", { user_id:'admin',password:'123456',name:"Admin" });
      server.create("notice", { title:"正式启动",content:"马上体验" });
      server.create("notice", { title:"Hello World",content:"Lorem Ipsum" });
      server.create("notice", { title:"主页，登陆，注册页",content:"采用bootstrap框架" });
      server.create("notice", { title:"Hello World",content:"Lorem Ipsum" });
      server.create("venue", { name:"新林院", 
      description:"First venue", 
      img:"https://miro.medium.com/max/1140/0*16bH8WYK3fOtu-kJ.jpg", 
      notice:[{ title:"闭馆通知",content:"请注意，11月15日闭馆" },{ title:"场地折扣10%",content:"即日起至12月1日" }]
      });
      server.create("venue", { name:"活动中心" , 
      description:"Normal venue", 
      img:"https://blog.playo.co/wp-content/uploads/2018/09/5b3f1476cb29c_badminton1.jpg",
      notice:[{ title:"闭馆通知",content:"小心了，11月15日闭馆" },{ title:"场地折扣5%",content:"只限马杯赛事场地" }]
    });
      
    },


  routes() {

    this.namespace = "api/v1";

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

    this.get("/main/notice", (schema) => {
      
      return schema.notices.all();
    
    });

    this.get("/venues/list", (schema) => {
      
      return schema.venues.all();
    
    });

    this.get("/venues/:id")
  }
  
})
  
  return server;
}