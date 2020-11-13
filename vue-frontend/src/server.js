import { Server, Model,Response  } from 'miragejs'

export function makeServer({ environment = "development" } = {}) {


let server = new Server({
  environment,

    models: {
      user: Model,
    },
    
    seeds(server) {
      server.create("user", { user_id:'admin',password:'123456',name:"Admin" });
    },


  routes() {

    this.namespace = "api/v1";

    this.post("/login", (schema,request) => {
      let attrs = JSON.parse(request.requestBody);

      let selected_user = schema.users.findBy({user_id:attrs.user_id});

      if(selected_user.password == attrs.password){
        return {"message":"ok"};
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
  
        return {"message":"ok"};
      }
      

    });
    
  },
  })
  
  
  return server
}