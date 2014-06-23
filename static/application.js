$( "#add_entry" ).submit(function( event ) {
    alert( "Handler for .submit() called." );
    event.preventDefault();
    var newTitle = $( "#title" ).val();
    var newText = $( "#text" ).val();
    $.ajax({
      type: "POST",
      url: "/add",
      data: { title: newTitle, text: newText }
    }).done(function( msg ) {
        alert( "Entry Added to DB, creating entry w/o repost...");
        var newEntryHtml = '<article class="entry" id="entry='+ msg.id + '">'
                                    +'<h3>' + msg.title + '</h3>'
                                    +'<p class="dateline">'+'Just Now'+'</p>'
                                    +'<div class="entry_body">'+msg.+'</div>'
                                    +'</article>';
        $("#entries").prepend(newEntryHtml);
      });
  });