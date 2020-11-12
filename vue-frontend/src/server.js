import { Server, Model } from 'miragejs'

export function makeServer({ environment = "development" } = {}) {


let server = new Server({
  environment,

    models: {
      person: Model,
      book:Model.extend(
          
      )
    },
    
    seeds(server) {
    server.create("person", { content: "Learn Mirage JS" })
    server.create("person", { content: "Integrate With Vue.js" })
    },


  routes() {

    this.namespace = "api/v1"

    this.get("/hello", schema => {
      return schema.people.all();
    })
    
  },
  })
  
  
  return server
}