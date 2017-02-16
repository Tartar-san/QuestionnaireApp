/**
 * Created by D1mD1m on 2/6/2017.
 */
$(document).ready(function () {

     $('.option-radio-lang').first().attr('required', '');
     $('.option-radio').first().attr('required', '');
       $('.option-input:checkbox').first().attr('required', '');
        $('.option-radio-lang').first().attr('oninvalid', "this.setCustomValidity('Виберіть мову / Выберите язык')");

       var langChoosing =  $('.option-radio-lang');
       if (langChoosing.length>0){
           $("#submitBtn").val("Відповісти / Ответить");
       }


        var tableContainers = $(".tableContainer");


 var userLang = $("html").attr("lang");// navigator.language || navigator.userLanguage;
        for(var i = 0; i< tableContainers.length ;  i++ ){
            tableContainers[i].children[0].children[0].required=true;


       switch(userLang){
           case 'uk':
                 tableContainers[i].children[0].children[0].setAttribute("oninvalid", "this.setCustomValidity('Виберіть відповідь')" );
                 //attr('oninvalid', "this.setCustomValidity('Виберіть відповідь')");
                 break;
           case 'ru':
               tableContainers[i].children[0].children[0].setAttribute("oninvalid", "this.setCustomValidity('Выберите ответ')" );

               break;
           default:
               break;
       }

            //console.log(children[i].firstChild());
        }


        setLangMessage();

         $('#mainForm').submit(function() {

             if(!isInputsChecked()) return false;

             if(!$('#mainForm')[0].checkValidity())return false;

         });

});



function setCookiesLikeTrue() {
    document.cookie = "Like=true";
    alert("liked");
}


function shareFBonClick(){
    FB.ui({
        method: 'feed',
        link: 'https://www.facebook.com/atlantynespisuyut/',
        //caption: 'An example caption'
    }, function(response){
        if (response === null) {
            console.log('was not shared');
        } else {
            setCookiesShareTrue();
        }
    });
}




function setCookiesShareTrue() {
    document.cookie = "Share=true";
    alert("shared");
}


function setLangMessage(className) {
    var userLang = $("html").attr("lang");// navigator.language || navigator.userLanguage;
       switch(userLang){
           case 'uk':
                $('.option-radio').first().attr('oninvalid', "this.setCustomValidity('Виберіть відповідь')");
                 $('.option-input:checkbox').first().attr('oninvalid', "this.setCustomValidity('Виберіть відповідь')");
                 $(className).first().attr('oninvalid', "this.setCustomValidity('Виберіть відповідь')");
               break;
           case 'ru':
                $('.option-radio').first().attr('oninvalid', "this.setCustomValidity('Выберите ответ')");
                 $('.option-input:checkbox').first().attr('oninvalid', "this.setCustomValidity('Выберите ответ')");
                 $(className).first().attr('oninvalid', "this.setCustomValidity(('Выберите ответ')");
               break;
           default:
               break;
       }
}


function isInputsChecked(){
     var isCheckBoxExist = $('.option-input:checkbox').length,
       checked =  $('.option-input:checkbox:checked').length > 0;
     return !isCheckBoxExist || checked;
}

  function toggleInvalidReset(className, reset) {
      if (isInputsChecked() || $(className).first().attr('oninvalid') !== "this.setCustomValidity('')") {
          $(className).first().attr('oninvalid', "this.setCustomValidity('')");
      } else {
          setLangMessage(className);

          // var userLang = $("html").attr("lang");// navigator.language || navigator.userLanguage;
          //  switch(userLang){
          //      case 'uk':
          //      //tableContainers[i].children[0].children[0].oninvalid = "this.setCustomValidity('Виберіть відповідь')";
          //        $(className).first().setAttribute("oninvalid", "this.setCustomValidity('Виберіть відповідь')" );
          //        break;
          //  case 'ru':
          //      $(className).first().setAttribute("oninvalid", "this.setCustomValidity('Выберите ответ')");
          //
          //      break;
          //  default:
          //      break;}

      }
  }
   function toggleRequired(className) {
      if (isInputsChecked()) {
          //$(className).first().removeAttr('required');
          $(className)[0].required=false;

      } else {
          $(className)[0].required=true;
          //$(className).first().attr('required', '');
      }
  }

