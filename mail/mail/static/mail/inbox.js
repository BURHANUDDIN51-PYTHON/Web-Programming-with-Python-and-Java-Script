document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-view').addEventListener('submit', (e) => {
    e.preventDefault();
    sendMail(document.querySelector('form'));
  });

  // By default, load the inbox
  load_mailbox('inbox');


 
    
  
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#specific-email').style.display='none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_email(mailbox){

  // Fetching the particular emails base on the mailbox
  fetch(`/emails/${mailbox}`)
  .then(res => res.json())
  .then(res => {
    show_email(res, mailbox);
  })
 
}

function viewMail(email_id){
    // Making a get fetch request for 
    fetch(`/emails/${email_id}`)
    .then(res => res.json())
    .then(res => {
        // Rendering the page 
        const el = document.createElement('div')
        const replyBtn = document.createElement('button')
        replyBtn.setAttribute("id", "#replybtn")
        replyBtn.className += 'btn btn-outline-primary'
        replyBtn.innerHTML = "Reply"
        el.innerHTML = `
              <div> 
                  <p><b>From:</b> ${res.sender}</p>  
                  <p><b>To:</b> ${res.recipients}</p>
                  <p><b>Subject:</b> ${res.subject}</p>
                  <p><b>TimeStamp:</b> ${res.timestamp}</p>      
                   <hr/>
                  <div>
                    <p>${res.body}</p>
                  </div>
            </div>
           
        `
        // Checking for the event listener
        replyBtn.addEventListener('click', () => replyMail(email_id))

        //Appending to the div tag
        el.append(replyBtn)
        document.querySelector('#specific-email').append(el);
        // Displaying the box
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#specific-email').style.display='block';
        document.querySelector('#compose-view').style.display = 'none';
    });
}

function show_email(data, mailbox){
  // Rendering the Data
  data.forEach((value) => {      
    const mainDiv = document.createElement('div');      
    mainDiv.className += 'pe-auto border border-secondary d-flex flex-row justify-content-between'; 
    // Changing the cursor on hover or mouseover
    mainDiv.addEventListener('mouseover', () => mainDiv.style.cursor = 'pointer');
    

    const el = document.createElement('div');
    el.className += `px-2 py-0 mb-1 d-flex flex-row justify-content-between align-items-center`;
    el.innerHTML = `
    <div class='d-flex flex-row justify-content-between align-items-center'>
      <p class='mx-1 '><b>${value.sender}</b></p>
      <p class='mx-1'> ${value.subject}</p>
    </div>
    <div class='ml-5 font-weight-bold'>
      <p>${value.timestamp}</p>
    </div>
    `
    mainDiv.append(el);
    if (mailbox === 'inbox' || mailbox =='archive'){
      const archiveBtn = document.createElement('button');
      archiveBtn.innerHTML = value.archived ? "Unarchive" : "Archive"
      archiveBtn.className += "btn btn-secondary m-2";
      mainDiv.append(archiveBtn)
      
      // Archive or Unarchive the mail using the event listner
      archiveBtn.addEventListener('click', () => {
        fetch(`/emails/${value.id}`, {
          method : "PUT",
          body: JSON.stringify({archived: !value.archived})
        })
        load_mailbox('inbox')
      })
    }
    // Checking whether the mail is readed or not 
    value.read ? mainDiv.style.backgroundColor = "whitesmoke" : mainDiv.style.backgroundColor = "#FF8225";
   
    el.addEventListener('click', () => {

      // Removing the existing Content
      document.querySelector('#specific-email').innerHTML = "";
      //Making a fetch request to change the read to true 
      fetch(`/emails/${value.id}`, {
        method: "PUT",
        body: JSON.stringify({read: true})
      })
      // Viewing the email
      viewMail(value.id)
    });
    
    document.querySelector("#emails-view").append(mainDiv);
  })
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#specific-email').style.display='none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Render the emails according to its respective mailbox
  load_email(mailbox)
}



function sendMail(form){
  // Getting the form Data
  const formData = new FormData(form);
  const formObject = {};

  formData.forEach((value, key) => {
    formObject[key] = value;
  });

  // Making a fetch request and posting the data at the backend
  // Posted successfully
  fetch('./emails', {
    method: "POST",
    body: JSON.stringify(formObject)
  })
  .then(res => res.json())
  .then(res => load_mailbox("sent"))

}

function replyMail(email_id){
    // Fetch the mail the data with the id
    fetch(`/emails/${email_id}`)
    .then(res => res.json())
    .then(res => {
      // render the compose page by using display
      console.log(res);
      compose_email()
      // fill the input field of the compose page with the content the mail you want to reply with
      
      document.querySelector('#compose-recipients').value = res.sender;
      // Add the condition to prevent Continous adding of Re
      if (res['subject'].split(' ')[0] != 'Re:') {
        document.querySelector('#compose-subject').value = `Re: ${res.subject}`;
      } else {
        document.querySelector('#compose-subject').value = res.subject;
      }
      document.querySelector('#compose-body').value = `On ${res.timestamp} ${res.sender} wrote: \n ${res.body}`
      
    })
    
}
