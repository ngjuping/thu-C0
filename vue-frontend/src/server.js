import { Server, Model,Response  } from 'miragejs'
import moment from 'moment'
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
              {start:"2020-11-26T12:00:00+01:00",end:"2020-11-26T13:00:00+01:00",code:3}]
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
    // 创建场馆
    this.post("/admin/create/venue", (schema, request) => {
      let attrs = JSON.parse(request.requestBody);
      console.log(schema.venues, 'schema');
      schema.venues.create(attrs);
      return { message:"ok" }
    })
    // 编辑场馆
    this.post("/admin/update/venue", (schema, request) => {
      let attrs = JSON.parse(request.requestBody);
      let selected_venues = schema.venues.findBy({id: attrs.id});
      selected_venues.update(attrs);
      return { message: 'ok' }
    })
    //access data: this.currentvenue = res.data.venue;
    this.get("/main/venues",(schema,request)=>{
      let selected_venue = schema.venues.findBy({id:request.queryParams.id});
      return {message:"ok",venue_info:selected_venue}
    })

    this.get("/booking",(schema,request)=>{
      
      let selected_venue = schema.venues.findBy({id:request.queryParams.id});
      
      return {venue_name:selected_venue.attrs.name,courts:selected_venue.attrs.courts};
    })
    // 增加新场地
    this.post('/admin/create/court', (schema, request) => {
      let attrs = JSON.parse(request.requestBody);
      let selected_venue = schema.venues.findBy({id: attrs.court[0].id});
      selected_venue.courts.push({
          id: selected_venue.courts.length + 1,
          status: attrs.court[0].status,
          type: attrs.court[0].type
      });
      console.log(selected_venue.courts, 'selected_venue')
      return { message:"ok" }
    })

    // 编辑场地
    this.post('/admin/update/court', (schema, request) => {
      let attrs = JSON.parse(request.requestBody);
      let selected_venue = schema.venues.findBy({id: attrs.court[0].id});
      selected_venue.courts = {
          id: attrs.court[0].id,
          status: attrs.court[0].status,
          type: attrs.court[0].type
      };
      console.log(selected_venue.courts, 'selected_venue')
      return { message:"ok" }
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
      return {message:"ok",reservation_id:1};
      
    });

    this.get('/manage/courts',(schema,request) => {
      console.log(request.queryParams.user_id);
      return {
        message:"ok",
        courts:[
        {
          reservation_id:1,
          type:1,
          details:{
            name: "新林院羽球场01",
            start:"2020-12-01T00:00:00+01:00",
            end:"2021-12-01T00:00:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:1,
          reviewed:0,
          shared:0
        },
        {
          reservation_id:2,
          type:3,
          details:{
            name: "活动中心网球场03",
            start:"2020-12-03T12:00:00+01:00",
            end:"2020-12-03T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:2,
          reviewed:1,
          shared:10
        },
        {
          reservation_id:3,
          type:2,
          details:{
            name: "活动中心乒乓球场04",
            start:"2021-12-30T12:00:00+01:00",
            end:"2021-12-30T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:1,
          reviewed:0,
          shared:11
        },
        {
          reservation_id:4,
          type:4,
          details:{
            name: "活动中心篮球场05",
            start:"2020-12-29T12:00:00+01:00",
            end:"2021-12-29T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:2,
          reviewed:0,
          shared:0
        },
        {
          reservation_id:5,
          type:1,
          details:{
            name: "新林院羽球场01",
            start:"2020-12-01T00:00:00+01:00",
            end:"2021-12-01T00:00:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:1,
          reviewed:0,
          shared:0
        },
        {
          reservation_id:6,
          type:3,
          details:{
            name: "活动中心网球场03",
            start:"2020-12-03T12:00:00+01:00",
            end:"2020-12-03T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:2,
          reviewed:1,
          shared:10
        },
        {
          reservation_id:7,
          type:2,
          details:{
            name: "活动中心乒乓球场04",
            start:"2021-12-30T12:00:00+01:00",
            end:"2021-12-30T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:3,
          reviewed:0,
          shared:11
        },
        {
          reservation_id:8,
          type:4,
          details:{
            name: "活动中心篮球场05",
            start:"2020-12-29T12:00:00+01:00",
            end:"2021-12-29T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:2,
          reviewed:0,
          shared:0
        },
        {
          reservation_id:9,
          type:1,
          details:{
            name: "新林院羽球场01",
            start:"2020-12-01T00:00:00+01:00",
            end:"2021-12-01T00:00:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:1,
          reviewed:0,
          shared:0
        },
        {
          reservation_id:10,
          type:3,
          details:{
            name: "活动中心网球场03",
            start:"2020-12-03T12:00:00+01:00",
            end:"2020-12-03T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:2,
          reviewed:1,
          shared:10
        },
        {
          reservation_id:11,
          type:2,
          details:{
            name: "活动中心乒乓球场04",
            start:"2021-12-30T12:00:00+01:00",
            end:"2021-12-30T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:1,
          reviewed:0,
          shared:11
        },
        {
          reservation_id:12,
          type:4,
          details:{
            name: "活动中心篮球场05",
            start:"2020-12-29T12:00:00+01:00",
            end:"2021-12-29T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:3,
          reviewed:0,
          shared:0
        },
        {
          reservation_id:13,
          type:2,
          details:{
            name: "活动中心乒乓球场04",
            start:"2021-12-30T12:00:00+01:00",
            end:"2021-12-30T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:3,
          reviewed:0,
          shared:11
        },
        {
          reservation_id:14,
          type:4,
          details:{
            name: "活动中心篮球场05",
            start:"2020-12-29T12:00:00+01:00",
            end:"2021-12-29T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:2,
          reviewed:0,
          shared:0
        },
        {
          reservation_id:15,
          type:1,
          details:{
            name: "新林院羽球场01",
            start:"2020-12-01T00:00:00+01:00",
            end:"2021-12-01T00:00:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:1,
          reviewed:0,
          shared:0
        },
        {
          reservation_id:16,
          type:3,
          details:{
            name: "活动中心网球场03",
            start:"2020-12-03T12:00:00+01:00",
            end:"2020-12-03T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:2,
          reviewed:1,
          shared:10
        },
        {
          reservation_id:17,
          type:2,
          details:{
            name: "活动中心乒乓球场04",
            start:"2021-12-30T12:00:00+01:00",
            end:"2021-12-30T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:1,
          reviewed:0,
          shared:11
        },
        {
          reservation_id:18,
          type:4,
          details:{
            name: "活动中心篮球场05",
            start:"2020-12-29T12:00:00+01:00",
            end:"2021-12-29T00:13:00+01:00",
            created: "2020-02-29T13:00:00+01:00",
            paid_at: "2020-02-29T13:10:00+01:00"
            },
          status:3,
          reviewed:0,
          shared:0
        },
        ]
        };
    });
    let all_notices = [{
      id:1,
      title: "title 1 超长标题等等等 测试标题对长标题的处理 无人爱苦，亦无人寻之欲之，乃因其苦...",
      content: "Lorem Ipsum，也称乱数假文或者哑元文本， 是印刷及排版领域所常用的虚拟文字。由于曾经一台匿名的打印机刻意打乱了一盒印刷字体从而造出一本字体样品书，Lorem Ipsum从西元15世纪起就被作为此领域的标准文本使用。它不仅延续了五个世纪，还通过了电子排版的挑战，其雏形却依然保存至今。在1960年代，”Leatraset”公司发布了印刷着Lorem Ipsum段落的纸张，从而广泛普及了它的使用。最近，计算机桌面出版软件”Aldus PageMaker”也通过同样的方式使Lorem Ipsum落入大众的视野。",
      time: moment().format()
    },
    {
      id:2,
      title: "title 2",
      content: "content 2"
    },
    {
      id:3,
      title: "title 3",
      content: "content 3"
    },
    {
      id:4,
      title: "title 4",
      content: "content 4"
    },
    {
      id:5,
      title: "title 5",
      content: "content 5"
    },
    {
      id:6,
      title: "title 6",
      content: "content 6"
    },
    {
      id:7,
      title: "title 7",
      content: "content 7"
    },
    {
      id:8,
      title: "title 8",
      content: "content 8"
    },
    {
      id:9,
      title: "title 9",
      content: "content 9"
    },
    {
      id:10,
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
    this.post("/admin/update/notice", (schema, request) => {
      let attrs = JSON.parse(request.requestBody);
      const index = all_notices.findIndex(item => item.id == attrs.id);
      all_notices[index] = attrs;
      return { message: 'ok' }
  })

  this.post("/admin/delete/notice", (schema, request) => {
      let attrs = JSON.parse(request.requestBody);
      const index = all_notices.findIndex(item => item.id == attrs.id);
      all_notices.splice(index, 1);
      return { message: 'ok' }
  })

  this.post("/admin/create/notice", (schema, request) => {
      let attrs = JSON.parse(request.requestBody);
      attrs.id = all_notices.length + 2;
      all_notices.push(attrs);
      console.log(all_notices, 'all_notices')
      return { message: 'ok' }
  })

    this.post('/manage/share/create',()=>{
      return {
        message:"ok",
        share_id:1
        }
      // return new Response(422, {}, { message: "系统繁忙" });
    })

    this.post('/manage/share/update',()=>{
      return {
        message:"ok",
        }
      // return new Response(422, {}, { message: "系统繁忙" });
    })
    
    this.post('/manage/share/delete',()=>{
      return {
        message:"ok",
        }
      // return new Response(422, {}, { message: "系统繁忙" });
    })


    this.post('/manage/reservation/cancel',()=>{

      return new Response(422, {}, { message: "场地不存在" });
    });

    this.post('/manage/feedback/create',(schema,request)=>{
      
      return {message:request,feedback_id:1};
    });

    this.post('/manage/feedback/update',()=>{
      
      return {message:"ok"};
    });

    this.post('/manage/feedback/delete',()=>{
      
      return {message:"ok"};
    });
    /**初始化场地 */
    // let all_courts = [
    //     {
    //       court_id: 1,
    //       price: 150,
    //       matrix: [
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0],
    //         [0,0,0,0,0,0,0]
    //       ]
    //     },
    //     {
    //         court_id: 2,
    //         price: 100,
    //         matrix: [
    //           [1,0,0,0,0,0,0],
    //           [0,1,0,0,0,0,0],
    //           [0,0,0,0,0,0,0],
    //           [0,0,0,0,0,0,0],
    //           [0,0,0,0,0,0,0],
    //           [0,0,0,0,0,0,0],
    //           [0,0,0,0,0,0,0],
    //           [0,0,0,0,0,0,0],
    //           [0,0,0,0,0,0,0],
    //           [0,0,0,0,0,0,0],
    //           [0,0,0,0,0,0,0],
    //           [0,0,0,0,0,0,0],
    //           [0,0,0,0,0,0,0],
    //           [0,0,0,0,0,0,0],
    //           [0,0,0,0,0,0,0]
    //         ]
    //     },
    // ]

    let all_courts = [
      {
          id: 1,
          name: '羽球场地',
          type: 1,
          venue: '1'
      },
      {
          id: 2,
          name: '篮球场地',
          type: 2,
          venue: ''
      }
  ]

  this.get('admin/court/list',(schema,request)=>{
      let requested_page = request.queryParams.page;
      if(requested_page < 1 || (requested_page-1)*5 > all_courts.length){
        return new Response(422, {}, { message: "页面不存在" });
      }
      return {
        message:"ok",
        total:all_courts.length,
        courts: all_courts.slice((requested_page-1)*5,(requested_page)*5)
      };
      
  });

    let all_feedbacks = [
      {
        user_id:1,
        feedback_id:1,
        content:"<blockquote><i>俗话说，有朋自远方来，不亦乐乎</i></blockquote><hr/><h1>这个场地是真的赞啦<b>666666</b><br/>服务很好</h1>",
        publish_date: "2013-03-01T00:00:00+01:00",
        court_id: 1,
        img: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/220px-Image_created_with_a_mobile_phone.png",
        reply: "非常感谢您",
        solved: 1,
        stars:5
      },
      {
        user_id:2,
        feedback_id:2,
        content:"场地很好",
        publish_date: "2013-03-01T00:00:00+01:00",
        court_id: 1,
        img: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/220px-Image_created_with_a_mobile_phone.png",
        reply: "感谢.........",
        solved: 1,
        stars:4
      },
      {
        user_id:1,
        feedback_id:3,
        content:"场地很好",
        publish_date: "2013-03-01T00:00:00+01:00",
        court_id: 2,
        img: "https://cdn1.i-scmp.com/sites/default/files/styles/768x768/public/images/methode/2018/07/17/70a0b93a-8973-11e8-8608-b7163509a377_1280x720_161847.JPG?itok=CMLKUPWf",
        solved: 0,
        stars:1
      },
      {
        user_id:1,
        feedback_id:4,
        content:"场地很好",
        publish_date: "2013-03-01T00:00:00+01:00",
        court_id: 2,
        img: "https://news.cgtn.com/news/3049544e7751544f776b7a4e3249444f776b7a4e31457a6333566d54/img/dbc2bed8083940c4a70ca53dc7e784a2/dbc2bed8083940c4a70ca53dc7e784a2.jpg",
        solved: 0,
        stars:2
      },
      {
        user_id:2,
        feedback_id:5,
        content:"场地不错",
        publish_date: "2013-03-01T00:00:00+01:00",
        court_id: 1,
        img: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/220px-Image_created_with_a_mobile_phone.png",
        reply: "非常感谢您",
        solved: 1,
        stars:1
      },
      {
        user_id:1,
        feedback_id:6,
        content:"场地很好",
        publish_date: "2013-03-01T00:00:00+01:00",
        court_id: 1,
        img: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/220px-Image_created_with_a_mobile_phone.png",
        reply: "感谢.........",
        solved: 0,
        stars:4
      },
      {
        user_id:1,
        feedback_id:7,
        content:"场地很好",
        publish_date: "2013-03-01T00:00:00+01:00",
        court_id: 2,
        img: "https://cdn1.i-scmp.com/sites/default/files/styles/768x768/public/images/methode/2018/07/17/70a0b93a-8973-11e8-8608-b7163509a377_1280x720_161847.JPG?itok=CMLKUPWf",
        solved: 0,
        stars:1
      },
      {
        user_id:1,
        feedback_id:8,
        content:"场地很好",
        publish_date: "2013-03-01T00:00:00+01:00",
        court_id: 2,
        img: "https://news.cgtn.com/news/3049544e7751544f776b7a4e3249444f776b7a4e31457a6333566d54/img/dbc2bed8083940c4a70ca53dc7e784a2/dbc2bed8083940c4a70ca53dc7e784a2.jpg",
        solved: 0,
        stars:5
      }
      ];
    this.get('manage/feedback',(schema,request)=>{
      let requested_page = request.queryParams.page;
      if(requested_page < 1 || (requested_page-1)*5 > all_feedbacks.length){
        return new Response(422, {}, { message: "页面不存在" });
      }
      return {
        message:"ok",
        total:all_feedbacks.length,
        feedbacks: all_feedbacks.slice((requested_page-1)*5,(requested_page)*5)
      };
      
    });

    this.get('manage/feedback/user',(schema,request)=>{
      var requested_user_id = parseInt(request.queryParams.user_id);
      var requested_page = parseInt(request.queryParams.page);
      let final_feedbacks = [];
      for(let i in all_feedbacks){
        if(all_feedbacks[i].user_id === requested_user_id){
          final_feedbacks.push(all_feedbacks[i]);
        }
      }
        return {
          message:"ok",
          total:final_feedbacks.length,
          feedbacks: final_feedbacks.slice((requested_page-1)*5,(requested_page)*5)
        }
      
    })
    this.post("/manage/feedback/delete", (schema, request) => {
      let attrs = JSON.parse(request.requestBody);
      const index = all_feedbacks.findIndex(item => item.feedback_id == attrs.feedback_id);
      all_feedbacks.splice(index, 1);
      return { message: 'ok' }
  })

  this.post("manage/feedback/create", (schema, request) => {
      let attrs = JSON.parse(request.requestBody);
      attrs.feedback_id = all_feedbacks.length + 2;
      attrs.user_id = all_feedbacks.length + 2;
      all_feedbacks.push(attrs);
      console.log(all_feedbacks, 'all_feedbacks')
      return { message: 'ok' }
  })

  this.post("/admin/reply/feedback", (schema, request) => {
      let attrs = JSON.parse(request.requestBody);
      const index = all_feedbacks.findIndex(item => item.feedback_id == attrs.feedback_id);
      console.log(index, 'index')
      all_feedbacks[index].reply = attrs.reply;
      all_feedbacks[index].solved = true;
      return { message: 'ok' }
  })
  let all_course = [
    {
        id: 1,
        name: 'qhy羽球课',
        price: '15元/hr'
    },
    {
        id: 2,
        name: 'qhy羽球课',
        price: '30元/hr'
    },
    {
        id: 3,
        name: 'qhy羽球课',
        price: '45元/hr'
    },
]

this.get('/courses',(schema,request)=>{
    let requested_page = request.queryParams.page;
    if(requested_page < 1 || (requested_page-1)*5 > all_course.length){
      return new Response(422, {}, { message: "页面不存在" });
    }
    return {
      message:"ok",
      total:all_course.length,
      courses: all_course.slice((requested_page-1)*5,(requested_page)*5)
    };
    
  });
  
  this.post("/admin/update/course", (schema, request) => {
    let attrs = JSON.parse(request.requestBody);
    const index = all_course.findIndex(item => item.id == attrs.id);
    all_course[index] = attrs;
    return { message: 'ok' }
  })

  this.post("/admin/delete/course", (schema, request) => {
      let attrs = JSON.parse(request.requestBody);
      const index = all_course.findIndex(item => item.id == attrs.id);
      all_course.splice(index, 1);
      return { message: 'ok' }
  })

  this.post("/admin/create/course", (schema, request) => {
      let attrs = JSON.parse(request.requestBody);
      attrs.id = all_course.length + 2;
      all_course.push(attrs);
      console.log(all_course, 'all_course')
      return { message: 'ok' }
  })


    let all_shares = [
      {
        user_id:1,
        share_id:1,
        content: "<h1>来和我一起打球</h1><blockquote><i>俗话说，有朋自远方来，不亦乐乎</i></blockquote><hr/><h3>来和最强的球手打球<b>666666</b><br/>不收钱</h3>",
        publish_date: "2020-12-01T8:00:00+01:00",
        reservation:{
        reservation_id:1,
        type:1,
        details:{
        name: "羽球场01",
        start: "2020-12-02T12:00:00+01:00",
        end:"2020-12-02T13:00:00+01:00"
        },
        status:1
        }
      },
      {
        user_id:1,
        share_id:2,
        content: "^_^来和我一起打球",
        publish_date: "2019-10-11T8:00:00+01:00",
        reservation:{
        reservation_id:2,
        type:1,
        details:{
        name: "羽球场02",
        start: "2020-12-02T12:00:00+01:00",
        end:"2020-12-02T13:00:00+01:00"
        },
        status:2
        }
      },
      {
        user_id:2,
        share_id:3,
        content: "来和我一起打球",
        publish_date: "2018-08-21T8:00:00+01:00",
        reservation:{
        reservation_id:1,
        type:1,
        details:{
        name: "网球场01",
        start: "2020-12-02T12:00:00+01:00",
        end:"2020-12-02T13:00:00+01:00"
        },
        status:2
        }
      }
    ]
    this.get('manage/share',(schema,request)=>{
      let requested_page = request.queryParams.page;
      if(requested_page < 1 || (requested_page-1)*5 > all_shares.length){
        return new Response(422, {}, { message: "页面不存在" });
      }
      return {
        message:"ok",
        total:all_shares.length,
        shares: all_shares.slice((requested_page-1)*5,(requested_page)*5)
      };
      
    });

    this.get('manage/share/user',(schema,request)=>{
      var requested_user_id = parseInt(request.queryParams.user_id);
      var requested_page = parseInt(request.queryParams.page);
      let final_shares = [];
      for(let i in all_shares){
        if(all_shares[i].user_id === requested_user_id){
          final_shares.push(all_shares[i]);
        }
      }
        return {
          message:"ok",
          total:final_shares.length,
          shares: final_shares.slice((requested_page-1)*5,(requested_page)*5)
        }
      
    })


    
    let users = [
      {
        user_id: 1,
        api_id: 'qiuyuhan-18',
        real_name: '邱俣涵'
      },
      {
        user_id: 2,
        api_id: 'huangzubin-19',
        real_name: '黄祖斌'
      },
      {
        user_id: 3,
        api_id: 'wangxuan-20',
        real_name: '王璇'
      },
      {
        user_id: 4,
        api_id: 'panbo-20',
        real_name: '潘嶓'
      },
      {
        user_id: 5,
        api_id: 'huangzhubin-18',
        real_name: '黄朱斌'
      },
      {
        user_id: 6,
        api_id: 'huangzubin-18',
        real_name: '黄祖斌'
      },
    ]

    this.post('manage/reservation/transfer',(schema,request)=>{
      let attrs = JSON.parse(request.requestBody);
      let target_user_id = parseInt(attrs.new_user_id);
      for(let i in users){
        if(users[i].user_id === target_user_id){
          return {
            message:"ok",
          }
        }
      }
      return new Response(422, {}, { message: "找不到用户" });
    })
    
    this.get('manage/getuserids',(schema,request)=>{
      var req_user_name = request.queryParams.user_name;
      let temp = [];
      for (let i in users){
        if(users[i].real_name.includes(req_user_name)){
          temp.push(users[i]);
        }
      } 
      return {
        message:"ok",
        users:temp
      }
      
    })

  this.post('pay/alipay',()=>{
    return new Response(404, {}, {message:"支付宝崩溃！不如试试微信支付？"});
    // return {
    //   message:"ok",
    // }
  })

  this.post('pay/wepay',()=>{
    return new Response(302, {'Location':'http://www.ngjuping.com'}, {});
    // return {
    //   message:"ok",
    // }
  })

  this.post('pay/offline',()=>{
    // return new Response(302, {'Location':'http://www.ngjuping.com'}, {});
    return {
      message:"ok",
    }
  })

  this.post('draw',()=>{
    //return new Response(302, {'Location':'http://www.ngjuping.com'}, {});
    return {
      message:"ok",
    }
  })
  }
  
})
  
  return server;
}