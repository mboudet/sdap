/* Functions */
function  get_filter_file(filter_by) {
    console.log(filter_by)
    $.ajax({
        url : filter_url,
        type: 'GET',
        data: {
            'filter_category':filter_by,
            'folder_id':folder_id,
        }
    });
};

