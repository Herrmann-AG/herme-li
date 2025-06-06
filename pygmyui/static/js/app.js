function copyToClipboard(className){
    var clipboard = new Clipboard('.' + className);
    clipboard.on('success', function(e) {
        console.log(e);
    });
    clipboard.on('error', function(e) {
        console.log(e);
    });
}


function readOnlyToggle(elementId) {
    var element = document.getElementById(elementId);
    element.value = '';
    element.readOnly = !element.readOnly;
}


function displayToggle(elementId) {
    var element = document.getElementById(elementId);
    var displayProperty = "block";
    if(element.style.display == displayProperty){
         displayProperty = "none";
    }
    element.style.display = displayProperty;
}

function validInput(input){
    // if invalid characters return false and change colour
    if (input != input.replace(/[^a-zA-Z0-9]/g, '')){
        var respText = "Ungültige Zeichen in der Eingabe";
        var checkButtonClass = "btn btn-sm btn-danger";
        var boxColor = 'red';
        document.getElementById('availableStatus').innerHTML = respText;
        document.getElementById('availableStatus').style.color = boxColor;
        document.getElementById('checkAvailable').className = checkButtonClass;
        return false;
    }
    return true;
}


function CheckLinkAvailability(){
    var customCodeInput = document.getElementById("customUrl");
    var customFormParentDiv = document.getElementById('customFormParentDiv');
    var customCode = customCodeInput.value.trim();
    document.getElementById('availableStatus').innerHTML = '';
    if(validInput(customCode) && customCode) {
        $.ajax({
            type: "GET",
            url: '/check',
            data: {custom_code: customCode},
            dataType: 'json',
            success:function(responsedata){
                var status = responsedata['ok'];
                var respText = 'Verfügbar!';
                var boxColor = 'green';
                var checkButtonClass = "btn btn-sm btn-primary";
                //var checkStatusIconClass = "glyphicon glyphicon-ok form-control-feedback";
                if(status == false) {
                    var respText = 'nicht verfügbar!';
                    var boxColor = 'red';
                    //var checkStatusIconClass = "glyphicon glyphicon-remove form-control-feedback";
                    var checkButtonClass = "btn btn-sm btn-danger";
                    // If not available focus and select
                    customFormParentDiv.className = 'form-group has-error';
                    customCodeInput.focus();
                    customCodeInput.select();
                } else {
                    customFormParentDiv.className = 'form-group has-success';
                    var checkButtonClass = "btn btn-sm btn-success";
                }
                document.getElementById('availableStatus').innerHTML = respText;
                document.getElementById('availableStatus').style.color = boxColor;
                document.getElementById('checkAvailable').className = checkButtonClass;
                //customCode.className = ''
                //document.getElementById('checkStatusIcon').className = checkStatusIconClass
            }
        })
    }
}

function DeleteLink(el){
    // Confirmation dialog before deleting link
    const confirmResponse = confirm('Are you sure you want to delete the link?');

    // Delete link if user confirmed
    if (confirmResponse) {
        var id = el.dataset.id.split("/").pop();
        
        $.ajax({
            type: "GET",
            url: '/remove',
            data: {link_id: id},
            dataType: 'json',
            success: function(responsedata){
                window.location.reload();
            }
        })
    };
};