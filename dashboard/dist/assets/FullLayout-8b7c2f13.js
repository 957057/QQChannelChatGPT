import{o,c as r,w as e,a as f,t as g,V as se,b as oe,d as t,e as H,f as I,g as B,h as W,i as J,j as K,r as U,k as Q,m as T,l as k,F as w,n as X,p as ne,q as A,s as ie,u,v as re,x as i,y as ue,z as x,A as Y,B as V,C as P,D as h,E as N,G as M,H as j,I as G,J as L,K as z,L as y,M as O,N as q,O as de,P as ce,Q as me,R as fe,S as ve,T as pe,U as _e,W as he,X as be}from"./index-a2f0b905.js";import{_ as Ve,u as $,m as F}from"./md5-f95c7b53.js";const ge=[{title:"面板",icon:"mdi-view-dashboard",to:"/dashboard/default"},{title:"配置",icon:"mdi-cog",to:"/config"},{title:"插件",icon:"mdi-puzzle",to:"/extension"},{title:"控制台",icon:"mdi-console",to:"/console"}],Z={__name:"NavGroup",props:{item:Object},setup(a){const n=a;return(d,_)=>(o(),r(se,{color:"darkText",class:"smallCap"},{default:e(()=>[f(g(n.item.header),1)]),_:1}))}},D={__name:"NavItem",props:{item:Object,level:Number},setup(a){return(n,d)=>(o(),r(K,{to:a.item.type==="external"?"":a.item.to,href:a.item.type==="external"?a.item.to:"",rounded:"",class:"mb-1",color:"secondary",disabled:a.item.disabled,target:a.item.type==="external"?"_blank":""},oe({prepend:e(()=>[a.item.icon?(o(),r(I,{key:0,color:a.item.iconColor,size:a.item.iconSize,class:"hide-menu",icon:a.item.icon},null,8,["color","size","icon"])):B("",!0)]),default:e(()=>[t(W,null,{default:e(()=>[f(g(a.item.title),1)]),_:1}),a.item.subCaption?(o(),r(J,{key:0,class:"text-caption mt-n1 hide-menu"},{default:e(()=>[f(g(a.item.subCaption),1)]),_:1})):B("",!0)]),_:2},[a.item.chip?{name:"append",fn:e(()=>[t(H,{color:a.item.chipColor,class:"sidebarchip hide-menu",size:a.item.chipIcon?"small":"default",variant:a.item.chipVariant,"prepend-icon":a.item.chipIcon},{default:e(()=>[f(g(a.item.chip),1)]),_:1},8,["color","size","variant","prepend-icon"])]),key:"0"}:void 0]),1032,["to","href","disabled","target"]))}},ye={__name:"IconSet",props:{item:Object,level:Number},setup(a){const n=a;return(d,_)=>n.level>0?(o(),r(U(n.item),{key:0,size:"5",fill:"currentColor","stroke-width":"1.5",class:"iconClass"})):(o(),r(U(n.item),{key:1,size:"20","stroke-width":"1.5",class:"iconClass"}))}},ee={__name:"NavCollapse",props:{item:Object,level:Number},setup(a){const n=a;return(d,_)=>{const p=Q("NavCollapse",!0);return o(),r(ne,{"no-action":""},{activator:e(({props:c})=>[t(K,T(c,{value:a.item.title,rounded:"",class:"mb-1",color:"secondary"}),{prepend:e(()=>[t(ye,{item:a.item.icon,level:a.level},null,8,["item","level"])]),default:e(()=>[t(W,{class:"mr-auto"},{default:e(()=>[f(g(a.item.title),1)]),_:1}),a.item.subCaption?(o(),r(J,{key:0,class:"text-caption mt-n1 hide-menu"},{default:e(()=>[f(g(a.item.subCaption),1)]),_:1})):B("",!0)]),_:2},1040,["value"])]),default:e(()=>[(o(!0),k(w,null,X(a.item.children,(c,v)=>(o(),k(w,{key:v},[c.children?(o(),r(p,{key:0,item:c,level:n.level+1},null,8,["item","level"])):(o(),r(D,{key:1,item:c,level:n.level+1},null,8,["item","level"]))],64))),128))]),_:1})}}},te={__name:"LogoMain",setup(a){return(n,d)=>(o(),r(Ve))}},ke={class:"pa-5"},Ce={class:"pa-4 text-center"},xe={name:"VerticalSidebar",components:{NavGroup:Z,NavItem:D,NavCollapse:ee,Logo:te},data:()=>({version:"-"}),mounted(){this.get_version()},methods:{get_version(){x.get("/api/stat/version").then(a=>{this.version=a.data.data.version}).catch(a=>{console.log(a)})}}},we=A({...xe,setup(a){const n=$(),d=ie(ge);return(_,p)=>{const c=Q("perfect-scrollbar");return o(),r(ue,{left:"",modelValue:i(n).Sidebar_drawer,"onUpdate:modelValue":p[0]||(p[0]=v=>i(n).Sidebar_drawer=v),elevation:"0","rail-width":"105","mobile-breakpoint":"960",app:"",class:"leftSidebar",rail:i(n).mini_sidebar,"expand-on-hover":""},{default:e(()=>[u("div",ke,[t(te)]),t(c,{class:"scrollnavbar"},{default:e(()=>[t(re,{class:"pa-4"},{default:e(()=>[(o(!0),k(w,null,X(d.value,(v,b)=>(o(),k(w,{key:b},[v.header?(o(),r(Z,{item:v,key:v.title},null,8,["item"])):v.divider?(o(),r(Y,{key:1,class:"my-3"})):v.children?(o(),r(ee,{key:2,class:"leftPadding",item:v,level:0},null,8,["item"])):(o(),r(D,{key:3,item:v,class:"leftPadding"},null,8,["item"]))],64))),128))]),_:1}),u("div",Ce,[t(H,{color:"inputBorder",size:"small"},{default:e(()=>[f(" v"+g(_.version),1)]),_:1})])]),_:1})]),_:1},8,["modelValue","rail"])}}}),Se={class:"mr-4"},Ne={key:0},ze={key:1},Ie=u("span",{class:"text-h5"},"更新项目",-1),Be=u("h3",{class:"mb-4"},"升级到最新版本",-1),Te={style:{"margin-top":"16px"}},Le=u("h3",{class:"mb-4"},"切换到指定版本或指定提交",-1),Ae=u("div",{class:"mb-4"},[u("small",null,"如 v3.3.16 (不带 SHA) 或 42e5ec5d80b93b6bfe8b566754d45ffac4c3fe0b"),u("br"),u("a",{href:"https://github.com/Soulter/AstrBot/commits/master"},[u("small",null,"查看 master 分支提交记录（点击右边的 copy 即可复制）")])],-1),$e=u("span",{class:"text-h5"},"密码修改",-1),De=u("small",null,"如果是第一次修改密码，原密码请留空。",-1),Re=u("br",null,null,-1),Ee=A({__name:"VerticalHeader",setup(a){const n=$();V(!1);let d=V(!1),_=V(!1),p=V(""),c=V(""),v=V(""),b=V(""),S=V(!1),C=V("");const ae=m=>{window.open(m,"_blank")};function le(){p.value!=""&&(p.value=F.md5(p.value)),c.value=F.md5(c.value),x.post("/api/auth/password/reset",{password:p.value,new_password:c.value}).then(m=>{if(m.data.status=="error"){v.value=m.data.message,p.value="",c.value="";return}d.value=!d.value,v.value=m.data.message,setTimeout(()=>{fe().logout()},1e3)}).catch(m=>{console.log(m),v.value=m,p.value="",c.value=""})}function R(){b.value="正在检查更新...",x.get("/api/update/check").then(m=>{S.value=m.data.data.has_new_version,b.value=m.data.message}).catch(m=>{console.log(m),b.value=m})}function E(m){b.value="正在切换版本...",x.post("/api/update/do",{version:m}).then(l=>{b.value=l.data.message,l.data.status=="success"&&setTimeout(()=>{window.location.reload()},1e3)}).catch(l=>{console.log(l),b.value=l})}return R(),(m,l)=>(o(),r(me,{elevation:"0",height:"80"},{default:e(()=>[t(h,{class:"hidden-md-and-down text-secondary",color:"lightsecondary",icon:"",rounded:"sm",variant:"flat",onClick:l[0]||(l[0]=P(s=>i(n).SET_MINI_SIDEBAR(!i(n).mini_sidebar),["stop"])),size:"small"},{default:e(()=>[t(I,null,{default:e(()=>[f("mdi-menu")]),_:1})]),_:1}),t(h,{class:"hidden-lg-and-up text-secondary ms-3",color:"lightsecondary",icon:"",rounded:"sm",variant:"flat",onClick:P(i(n).SET_SIDEBAR_DRAWER,["stop"]),size:"small"},{default:e(()=>[t(I,null,{default:e(()=>[f("mdi-menu")]),_:1})]),_:1},8,["onClick"]),t(N),u("div",Se,[i(S)?(o(),k("small",Ne," 有新版本！ ")):(o(),k("small",ze," 当前版本已是最新 "))]),t(q,{modelValue:i(_),"onUpdate:modelValue":l[5]||(l[5]=s=>y(_)?_.value=s:_=s),width:"700"},{activator:e(({props:s})=>[t(h,T({onClick:R,class:"text-primary mr-4",color:"lightprimary",variant:"flat",rounded:"sm"},s),{default:e(()=>[f(" 更新 🔄 ")]),_:2},1040)]),default:e(()=>[t(M,null,{default:e(()=>[t(j,null,{default:e(()=>[Ie]),_:1}),t(G,null,{default:e(()=>[t(L,null,{default:e(()=>[Be,u("p",null,g(i(b)),1),t(h,{class:"mt-4 mb-4",onClick:l[1]||(l[1]=s=>E("latest")),color:"primary",style:{"border-radius":"10px"},disabled:!i(S)},{default:e(()=>[f(" 更新到最新版本 ")]),_:1},8,["disabled"]),t(Y),u("div",Te,[Le,t(z,{label:"输入版本号或 master 分支下的 commit hash。",modelValue:i(C),"onUpdate:modelValue":l[2]||(l[2]=s=>y(C)?C.value=s:C=s),required:"",variant:"outlined"},null,8,["modelValue"]),Ae,t(h,{color:"error",style:{"border-radius":"10px"},onClick:l[3]||(l[3]=s=>E(i(C)))},{default:e(()=>[f(" 确定切换 ")]),_:1})])]),_:1})]),_:1}),t(O,null,{default:e(()=>[t(N),t(h,{color:"blue-darken-1",variant:"text",onClick:l[4]||(l[4]=s=>y(_)?_.value=!1:_=!1)},{default:e(()=>[f(" 关闭 ")]),_:1})]),_:1})]),_:1})]),_:1},8,["modelValue"]),t(q,{modelValue:i(d),"onUpdate:modelValue":l[9]||(l[9]=s=>y(d)?d.value=s:d=s),persistent:"",width:"700"},{activator:e(({props:s})=>[t(h,T({class:"text-primary mr-4",color:"lightprimary",variant:"flat",rounded:"sm"},s),{default:e(()=>[f(" 密码修改 📰 ")]),_:2},1040)]),default:e(()=>[t(M,null,{default:e(()=>[t(j,null,{default:e(()=>[$e]),_:1}),t(G,null,{default:e(()=>[t(L,null,{default:e(()=>[t(de,null,{default:e(()=>[t(ce,{cols:"12"},{default:e(()=>[t(z,{label:"原密码*",type:"password",modelValue:i(p),"onUpdate:modelValue":l[6]||(l[6]=s=>y(p)?p.value=s:p=s),required:"",variant:"outlined"},null,8,["modelValue"]),t(z,{label:"新密码*",type:"password",modelValue:i(c),"onUpdate:modelValue":l[7]||(l[7]=s=>y(c)?c.value=s:c=s),required:"",variant:"outlined"},null,8,["modelValue"])]),_:1})]),_:1})]),_:1}),De,Re,u("small",null,g(i(v)),1)]),_:1}),t(O,null,{default:e(()=>[t(N),t(h,{color:"blue-darken-1",variant:"text",onClick:l[8]||(l[8]=s=>y(d)?d.value=!1:d=!1)},{default:e(()=>[f(" 关闭 ")]),_:1}),t(h,{color:"blue-darken-1",variant:"text",onClick:le},{default:e(()=>[f(" 提交 ")]),_:1})]),_:1})]),_:1})]),_:1},8,["modelValue"]),t(h,{class:"text-primary mr-4",onClick:l[10]||(l[10]=s=>ae("https://github.com/Soulter/AstrBot")),color:"lightprimary",variant:"flat",rounded:"sm"},{default:e(()=>[f(" GitHub Star! 🌟 ")]),_:1})]),_:1}))}}),Me=A({__name:"FullLayout",setup(a){const n=$();return(d,_)=>(o(),r(he,null,{default:e(()=>[t(_e,{theme:"PurpleTheme",class:pe([i(n).fontTheme,i(n).mini_sidebar?"mini-sidebar":"",i(n).inputBg?"inputWithbg":""])},{default:e(()=>[t(we),t(Ee),t(ve,null,{default:e(()=>[t(L,{fluid:"",class:"page-wrapper"},{default:e(()=>[u("div",null,[t(i(be))])]),_:1})]),_:1})]),_:1},8,["class"])]),_:1}))}});export{Me as default};