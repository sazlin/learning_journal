$( "#add_entry" ).submit(function( event ) {
    alert( "Handler for .submit() called." );
    event.preventDefault();
    $.post({
      type: "POST",
      url: "/add",
      data: "This is some data"
    });
  });