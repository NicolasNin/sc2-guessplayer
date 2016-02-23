//rest input field
$(function (){
	
		$("#test3").val("");
		$("#test2").val("");
		
	});

$(function () { $('#test2').change(function() 
				{ 
					$('#modal-body').html("uploading"); 
					$('#myModal').modal({
					show: 'true'
						}); 
				 // get the current value of the input field.
				console.log($(this).val())
				//upload using ajax jquery and formdata
				 var $form=$('#my_form')
			     var formdata = (window.FormData) ? new FormData($form[0]) : null;
			     var data = (formdata !== null) ? formdata : $form.serialize();
				 $.ajax(
			        {
			            url: $form.attr('action'),
			            type: $form.attr('method'),
			            contentType: false, // obligatoire pour de l'upload
			            processData: false, // obligatoire pour de l'upload
			            dataType: 'text', // selon le retour attendu
			            data: data,
			            success: function (response) 
			            {
							
							console.log(response)
							if( response=="error with the file")
							{
								$('#test2').val("");
								$('#modal-body').html("error with the files"); 
							
								
								
							}else{
							
							document.getElementById("file-uploaded").value=response;
							document.getElementById("hiddenform").submit();
						}
			            }
			        });
				//
				
				});
				
			});
			
			
$(function () { $('#test3').change(function() 
				{ 
					$('#modal-body').html("uploading"); 
					$('#myModal').modal({
					show: 'true'
						}); 
				 // get the current value of the input field.
				console.log($(this).val())
				//upload using ajax jquery and formdata
				 var $form=$('#my_form3')
			     var formdata = (window.FormData) ? new FormData($form[0]) : null;
			     var data = (formdata !== null) ? formdata : $form.serialize();
				 $.ajax(
			        {
			            url: $form.attr('action'),
			            type: $form.attr('method'),
			            contentType: false, // obligatoire pour de l'upload
			            processData: false, // obligatoire pour de l'upload
			            dataType: 'text', // selon le retour attendu
			            data: data,
			            success: function (response) 
			            {
							console.log(response)
							if( response=="error with the file")
							{	$('#test3').val("");
								$('#modal-body').html("error with the files"); 
								//document.getElementById('test3').value="";
								}
							else{
							document.getElementById("file-uploaded").value=response;
							document.getElementById("hiddenform").submit();
						}
			                
			            }
			        });
				//
				
				});
				
			});
						
