$(document).ready(function () {
    $("#id_datepicker").datepicker({  
        autoclose: true,  
        todayHighlight: true, 
        todayBtn : "linked",  
    }).datepicker('update', new Date()); 
    $(".toast").each(function () {
        let toast = $(this);
        $(toast).toast({
            autohide:false
        })
        $(toast).toast('show');
        $(toast).find("button").each(function () {
            $(this).on("click", function () {
                $(toast).toast("hide");
            });
        });
    });
});