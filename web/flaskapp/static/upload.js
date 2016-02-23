$(function () { $('#test2').change(function() 
				{ 
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
							{alert("error")}
							
							document.getElementById("file-uploaded").value=response;
							document.getElementById("hiddenform").submit();
			                
			            }
			        });
				//
				
				});
				
			});
			
			
$(function () { $('#test3').change(function() 
				{ 
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
							{alert("error")}
							
							document.getElementById("file-uploaded").value=response;
							document.getElementById("hiddenform").submit();
			                
			            }
			        });
				//
				
				});
				
			});
						
