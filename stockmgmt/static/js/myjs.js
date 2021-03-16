$(document).ready(function(){

    $(".table").paging({limit:8});
    $(".datetimeinput").datepicker({changeYear: true, changeMonth:true, dateformat: 'yy-mm-dd'});
});