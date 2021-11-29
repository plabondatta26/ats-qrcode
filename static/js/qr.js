function add_mobile() {
    // alert('ok');
    var new_chq_no = parseInt($('#total_chq').val()) + 1;
    var new_input = "<input type='text' id='new_" + new_chq_no + "'>";
    $('#new_chq').html(new_input);
}