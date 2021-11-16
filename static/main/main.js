
function like(postId){

        csrftoken = getCookie('csrftoken');

        $.ajax({
            headers:{'X-CSRFToken':csrftoken},
            type: "post",
            url: "/create_like/",
            data:{'post_id': postId},
            success: function (response) {
                
                $('#likecount_'+postId).html(response.likes)

            }
    });

}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



function commentSection(postId){
    csrftoken = getCookie('csrftoken');
    $.ajax({
        headers:{'X-CSRFToken':csrftoken},
        type: "get",
        url: "/comment/",
        data:{'post_id': postId},
        success: function (response) {
           
            commentslist = "";
            for (let index = 0; index < response.comments.length; index++) {
                
                comments = response.comments[index].fields
                commentslist += "<div class='commentBox mb-1'>"+"<span class='commentUser'>"+response.name[index].first_name+
                                " "+response.name[index].last_name+"</span><br>"+comments.comment+"<br>"+
                                "<span class='commentDelete'><a onclick='deleteComment("+response.comments[index].pk+
                                ","+ postId+")'>Delete</a></span>"+
                                "</div>" ;
            }
           
            $('#commentsList_'+postId).html(commentslist);
            $('#commentcount_'+postId).html(response.commentCount);
            closeUpdateForm(postId);
            $('#commentSection_'+postId).show();

            
        }
       
});

   
}

function closeComments(postId){
    $('#commentSection_'+postId).hide();

}

function checkButton(postId) {
    csrftoken = getCookie('csrftoken');
    const commentData =$('#commentSection_'+postId).find('input[name="comment"]').val();
    
    $.ajax({
        headers:{'X-CSRFToken':csrftoken},
        type: "post",
        url: "/comment/",
        data:{'post_id': postId,
              'commentData':commentData},
        success: function (response) {  
            commentSection(postId);   
        }
    });
}

function comment(postId){

    /*csrftoken = getCookie('csrftoken');
    const commentData =$('#commentSection_'+postId).find('input[name="comment"]').val();
    alert(postId+""+commentData);
   
    $.ajax({
        headers:{'X-CSRFToken':csrftoken},
        type: "post",
        url: "/comment/",
        data:{'post_id': postId,
              'commentData':commentData},
        success: function (response) {  
            commentSection(postId);   
        }
    });
*/
}

function deleteComment(id, postId){

    $.ajax({
        headers:{'X-CSRFToken':csrftoken},
        type: "post",
        url: "/delete_comment/",
        data:{'id': id},
        success: function (response) {  
            commentSection(postId);
        }
    });
}


function getPosts(posts){
 
    $.ajax({
        type: "get",
        url: "/user/",
        success: function (response) { 
           
            
                posts(response);
            
           
          
        }
    });
}


function getPost(postId, post){

    $.ajax({
        type: "get",
        url: "/show_post/",
        data: {'postId':postId},
        success: function (response) {
         data = response;
         post(data);

        }
    });
}
 

function showUpdateForm(postId){

    getPost(postId, function(response){
        closeComments(postId);
        $('#postUpdateForm_'+postId).find('[name="post"]').val(response.post[0].fields.post);
        $('#postUpdateForm_'+postId).show();
        $('#updatePostButton').attr('onclick','updatePost('+postId+')');
    });
    
    
   

}

function updatePost(postId){

    var updatedPost =$('#postUpdateForm_'+postId).find('[name="post"]').val();
    var image = $('#postUpdateForm_'+postId).find('[name="image"]')[0].files[0];
    var formData = new FormData();
    formData.append('updatedImage',image)
    formData.append('postId',postId)
    formData.append('updatedPost',updatedPost)
    var csrftoken = getCookie('csrftoken')
    $.ajax({
        headers:{'X-CSRFToken':csrftoken},
        type: "post",
        url: "/update_post/",
        data: formData,
        enctype:'mutlipart/form-data',
        contentType: false,
        processData: false,
        
        success: function () {
            getPost(postId, function(data){
                $('#postContent_'+postId).html(data.post[0].fields.post); 
                $('#postImage_'+postId).attr('src','/media/'+data.post[0].fields.image);
            });
            
            closeUpdateForm(postId);
           
        }
    }); 

}

function closeUpdateForm(postId){
    $('#postUpdateForm_'+postId).hide();
}
 
$(document).ready(function(){
    $('form#updateProfile').on('submit',function(){
        var image = $(this).find('[name="image"]')[0].files.length;
        if(image === 0){
            alertify.error('please select image ');
            return false
        }
    });
});

