$(document).ready(function () {
    $("#id_datepicker").datepicker({  
        autoclose: true,  
        todayHighlight: true, 
        todayBtn : "linked",  
    }).datepicker('update', new Date()); 
});