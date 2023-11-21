class ExpandRowButton{
    constructor(jqueryObject) {
        this.button = $(jqueryObject);
        this.parentRow = this.button.parent().parent();
        this.bodyRow = this.parentRow.next();
        this.time = 500;
    }

    toggleRow = () => {
        if(this.parentRow.attr("expanded") === "true"){
            this.bodyRow.slideUp("slow");
            this.bodyRow.addClass("d-none");
            this.parentRow.attr("expanded", "false");
        }
        else if(this.parentRow.attr("expanded") === "false"){
            this.bodyRow.slideDown("slow");
            this.bodyRow.removeClass("d-none");
            this.parentRow.attr("expanded", "true");
        }
    }
}

function registerExpandRowButton() {
    let buttonHandler = new ExpandRowButton($(this));
    $(this).click(buttonHandler.toggleRow);
}

$(document).ready(function () {
    $(".expandRowBtn").each(registerExpandRowButton);
});