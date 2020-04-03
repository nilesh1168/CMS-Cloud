var answers = [];
var cnt=0;
console.log(document.getElementById("session").textContent)
const registerServiceWorker = async () => {
  swRegistration =  await navigator.serviceWorker.register('service-worker.js');
  return swRegistration;
}

const requestNotificationPermission = async () => {
const permission = await window.Notification.requestPermission();
// value of permission can be 'granted', 'default', 'denied'
// granted: user has accepted the request
// default: user has dismissed the notification permission popup by clicking on x
// denied: user has denied the request.
if(permission !== 'granted'){
    throw new Error('Permission not granted for Notification');
}
}

const check = () => {
  if (!('serviceWorker' in navigator)) {
    throw new Error('No Service Worker support!')
  }
  if (!('PushManager' in window)) {
    throw new Error('No Push API Support!')
  }
  
}

const showLocalNotification = (title, body, tag, swRegistration) => {
  const options = {
      body : body,
      tag : tag,
      vibrate : [200,100,200]
  };
 swRegistration.showNotification(title, options);
}

async function Q1(swRegistration){
  return new Promise((resolve)=>{
    setTimeout(() => {
      resolve(showLocalNotification('Question 1', 'Is the venue easily accessible?',1, swRegistration));
    }, 3000);
  });
}

async function Q2(swRegistration){
  return new Promise((resolve)=>{
    setTimeout(() => {
      resolve(showLocalNotification('Question 2', 'Is the Session Interactive?',2, swRegistration));
    }, 6000);
  });
}

async function Q3(swRegistration){
  return new Promise((resolve)=>{
    setTimeout(() => {
      resolve(showLocalNotification('Question 3', 'Does the Instructor demonstrate adequate knowledge of topic?',3, swRegistration));
    }, 9000);
  });
}

async function Q4(swRegistration){
  return new Promise((resolve)=>{
    setTimeout(() => {
      resolve(showLocalNotification('Question 4', 'Was the Seminar relevant to the topic?',4, swRegistration));
    }, 12000);
  });
}

async function Q5(swRegistration){
  return new Promise((resolve)=>{
    setTimeout(() => {
      resolve(showLocalNotification('Question 5', 'Are you likely to participate in our future seminar sessions?',5, swRegistration));
    }, 15000);
  });
}

const main = async() => {
  check();
  console.log(document.getElementById("session").textContent);
  swRegistration = await registerServiceWorker();
  const permission =  await requestNotificationPermission();
  await Q1(swRegistration);
  await Q2(swRegistration);
  await Q3(swRegistration);
  await Q4(swRegistration);
  await Q5(swRegistration);   
  console.log("Heello");
  
}


navigator.serviceWorker.addEventListener("message", function (event) {
  console.log("in navigator client: "+event.data.tag);
  if(event.data.tag == 1)
  {
    console.log("First Question!!");
    $('#myModal1').modal();
    $("#close1").click(function (e) { 
          var ans1 = $('input[name=groupOfDefaultRadios1]:checked').val();
          answers.push(ans1);
          console.log(answers); 
          $('#myModal1').modal('hide');
        });
        cnt+=1;
        console.log(cnt);
        if(cnt==5)
  {
    $.ajax({
      type: "post",
      url: "/feedback_form",
      data: "data="+answers+"&session="+document.getElementById("session").textContent,
      success: function (response) {
        document.write(response);
      }
    });
  }
  }
  else if (event.data.tag == 2) {
    console.log("SECOND Q");
    $('#myModal2').modal();
    $("#close2").click(function (e) { 
      var ans1 = $('input[name=groupOfDefaultRadios2]:checked').val();
      answers.push(ans1);
      console.log(answers); 
      $('#myModal2').modal('hide');
      cnt+=1;
        console.log(cnt);
        if(cnt==5)
  {
    $.ajax({
      type: "post",
      url: "/feedback_form",
      data: "data="+answers+"&session="+document.getElementById("session").textContent,
      success: function (response) {
        document.write(response);
      }
    });
  }
    });

  }else if (event.data.tag == 3) {
    console.log("THIRD Q");
    $('#myModal3').modal();
    $("#close3").click(function (e) { 
      var ans1 = $('input[name=groupOfDefaultRadios3]:checked').val();
      answers.push(ans1);
      console.log(answers);
      $('#myModal3').modal('hide');
      cnt+=1;
        console.log(cnt); 
        if(cnt==5)
  {
    $.ajax({
      type: "post",
      url: "/feedback_form",
      data: "data="+answers+"&session="+document.getElementById("session").textContent,
      success: function (response) {
        document.write(response);
      }
    });
  }
    });
  } else if (event.data.tag == 4) {
    console.log("FOURTH Q");
    $('#myModal4').modal();
    $("#close4").click(function (e) { 
      var ans1 = $('input[name=groupOfDefaultRadios4]:checked').val();
      answers.push(ans1);
      console.log(answers);
      $('#myModal4').modal('hide');
      cnt+=1;
      console.log(cnt); 
      if(cnt==5)
  {
    $.ajax({
      type: "post",
      url: "/feedback_form",
      data: "data="+answers+"&session="+document.getElementById("session").textContent,
      success: function (response) {
        document.write(response);
      }
    });
  }
    });
  } else if(event.data.tag == 5){
    console.log("FIFTH Q");
    $('#myModal5').modal();
    $("#close5").click(function (e) { 
      var ans1 = $('input[name=groupOfDefaultRadios5]:checked').val();
      answers.push(ans1);
      console.log(answers); 
      $('#myModal5').modal('hide');
      cnt+=1;
      console.log(cnt);
      if(cnt==5)
  {
    $.ajax({
      type: "get",
      url: "/feedback_form",
      data: "data="+answers+"&session="+document.getElementById("session").textContent,
      success: function (response) {
          console.log('SUCCESS');
          document.write(response);
      }
    });
  }
    });
  }
});
