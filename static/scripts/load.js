$(document).ready(function () {
    $('button').on('click', function () {
      $('#userinfo').html("")
      $('#listofmatches').html("")
      $('#same_utc').html("")
        $.ajax({
            type: 'GET',
            url: '/main_user/' + $('input').val(),
            dataType:"json",
            beforeSend: function (xhr) {
              make_spinner();
            },
            success: function (data) {
              console.log(data)
              let content = ''
                content += '<img src="' + data.photo + '" style=width:100%;>'
                content += '<h2>' + data.name + '</h2>'
                content += '<p id="user_tz">' + data.timezone +'</p>'
                $('#userinfo').html(content)
              data_table(data.timezone)
            }
        });
      console.log('Done!!!!');
    });
  });

  function data_table(timezone) {
    $.ajax({
            type: 'GET',
            url: '/same_utc/?timezone=' + timezone,
            dataType:"html",
            success: function (data) {
              $('#same_utc').html(data)
              let table = document.querySelector('.dataframe')
              table.classList.add('table')
              $('#spinner').html('')
            }
          });
  }

  function make_spinner() {
    sppiner = ''
    sppiner += '<div id="spinner" class="pt-5" style="margin-left:50%">'
      sppiner += '<div class="spinner-border text-light" style="width: 3rem; height: 3rem;" role="status">'
        sppiner += '<span class="sr-only" style="margin-left:50%">Loading...</span>'
      sppiner += '</div>'
      sppiner += '<h1 class="text-light font-weight-bold pt-5" style="margin-left:-30%">'
        sppiner += 'Finding jobs at your time zone'
      sppiner += '</h1>'
    sppiner += '</div>'
    $('#spinner').html(sppiner)
  }