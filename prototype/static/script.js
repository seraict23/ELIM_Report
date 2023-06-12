let usagechange_row = 0;
let structurechange_row=0;
let environmentchange=0;
let expansion_row=0;
let overload=0;
let accident=0;

let fd = new FormData();


$("#temporary").on("click", function () {
  fd.append("usagechange-length", usagechange_row)
  if(usagechange_row !== 0) {
    for (let i = 1; i <= usagechange_row; i++) {
      for (let j = 1; j <= 7; j++) {
        fd.append(
          "usagechange-"+i.toString(),
          $("input[name=1-" + i.toString() + "-" + j.toString() + "]").val()
        );
      }
    }
  }

  
  fd.append("structurechange-length", structurechange_row)
  if(structurechange_row !==0 ){
    for (let i = 1; i <= structurechange_row; i++) {
      for (let j = 1; j <= 7; j++) {
        fd.append(
          "structurechange-"+i.toString(),
          $("input[name=2-" + i.toString() + "-" + j.toString() + "]").val()
        );
      }
    }
  }

  fd.append("environmentchange", environmentchange)
  if (environmentchange!==0) {
    for (let i = 1; i <=3; i++){
      for (let j = 1; j<=3; j++){
        fd.append("environmentchange-"+i.toString(), $("input[name=3-"+i.toString()+"-"+j.toString()+"]").val())
      }
    }
  }

  
  fd.append("expansion-length", expansion_row)
  if(expansion_row!==0) {
    for (let i = 1; i <= expansion_row; i++) {
      for (let j = 1; j <= 7; j++) {
        fd.append(
          "expansion-"+i.toString(),
          $("input[name=4-" + i.toString() + "-" + j.toString() + "]").val()
        );
      }
    }
  }

  fd.append("overload",overload)
  if(overload>0) {
    fd.append("overload", $("input[name=5-5-1]").val());
  }
  
  fd.append("accident", accident)
  if(accident>0) {
    for(let j=1;j<=6;j++){
      fd.append("accident",  $("input[name="+j.toString()+"-1-1]").val())
    }
  }

  $.ajax({
    url: "/chapter2/temporary/",
    data: fd,
    method: "POST",
    processData: false,
    contentType: false,
    success: () => {
      console.log("성공");
    },
    error: (req, status, err) => {
      console.log(err);
    },
    complete: () => {
      console.log("완료");
    },
  });
});

// 1.용도변경; 테이블 행 추가 및 동적 할당
$("#1-usagechange-appendrow-button").on("click", () => {
  usagechange_row++;
  const row = usagechange_row
  $("#1-usagechange-appendrow").append(
    '<div class="row">' +
      '<div class="col"><input class="input-in-grid" name="1-' +
      row.toString() +
      '-1"/></div>' +
      '<div class="col-4"><div class="container text-center"><div></div><div class="row">' +
      '<div class="col-8"><input class="input-in-grid" name="1-' +
      row.toString() +
      '-2"/></div>' +
      '<div class="col"><input class="input-in-grid" name="1-' +
      row.toString() +
      '-3"/></div>' +
      "</div></div></div>" +
      '<div class="col-4"><div class="container text-center"><div></div><div class="row">' +
      '<div class="col-8"><input class="input-in-grid" name="1-' +
      row.toString() +
      '-4"/></div>' +
      '<div class="col"><input class="input-in-grid" name="1-' +
      row.toString() +
      '-5"/></div>' +
      "</div></div></div>" +
      '<div class="col"><input class="input-in-grid" name="1-' +
      row.toString() +
      '-6"/></div>' +
      '<div class="col"><input class="input-in-grid" name="1-' +
      row.toString() +
      '-7"/></div>' +
      "</div>"
  );
});

// 2.구조변경; 테이블 향 추가 및 동적 할당
$("#2-structurechange-appendrow-button").on("click", () => {
  structurechange_row++;
  const row = structurechange_row.toString()
  $("#2-structurechange-appendrow").append(
    '<div class="row">'+
    '<div class="col"><input class="input-in-grid" name="2-'+row.toString()+'-1" /></div>'+
    '<div class="col"><input class="input-in-grid" name="2-'+row.toString()+'-2"/></div>'+
    '<div class="col"><input class="input-in-grid" name="2-'+row.toString()+'-3"/></div>'+
    '<div class="col-2"><input class="input-in-grid" name="2-'+row.toString()+'-4"/></div>'+
    '<div class="col-3"><input class="input-in-grid" name="2-'+row.toString()+'-5"/></div>'+
    '<div class="col"><input class="input-in-grid" name="2-'+row.toString()+'-6"/></div>'+
    '<div class="col"><input class="input-in-grid" name="2-'+row.toString()+'-7"/></div>'+
    '</div>'
  );
});

$("#4-expansion-appendrow-button").on("click", () => {
  expansion_row++;
  const row = expansion_row.toString()
  $("#4-expansion-appendrow").append(
    '<div class="row">'+
    '<div class="col"><input class="input-in-grid" name="4-'+row.toString()+'-1"/></div>'+
    '<div class="col-4"><div class="container text-center"><div class="row"></div><div class="row">'+
    '<div class="col-8"><input class="input-in-grid" name="4-'+row.toString()+'-2"/></div>'+
    '<div class="col"><input class="input-in-grid" name="4-'+row.toString()+'-3"/></div>'+
    '</div></div></div>'+
    '<div class="col-4"><div class="container text-center"><div></div><div class="row">'+
    '<div class="col-8"><input class="input-in-grid" name="4-'+row.toString()+'-4"/></div>'+
    '<div class="col-4"><input class="input-in-grid" name="4-'+row.toString()+'-5"/></div>'+
    '</div></div></div>'+
    '<div class="col"><input class="input-in-grid" name="4-'+row.toString()+'-6"/></div>'+
    '<div class="col"><input class="input-in-grid" name="4-'+row.toString()+'-7"/></div>'+
    '</div>'
  );
});


/* Checkbox change event */
$("#1-usagechange").change(function () {
  var value = $(this).val();
  if (value == "yes") {
    $("#1-usagechange-table").css({ display: "flex" });
    usagechange_row++;
  } else {
    $("#1-usagechange-table").css({ display: "none" });
    usagechange_row=0;
  }
});

$("#1-usagechange-btn").on("click", function () {
  $(".1-square-inner").css({ display: "block", "padding-bottom": "80%" });
  $("#1-usagechange-images").css({ display: "flex" });
  $("#1-usagechange-btn").css({ display: "none" });
  $("#1-usagechange-btn2").css({ display: "block" });
});

$("#2-structurechange").change(function () {
  var value = $(this).val();
  if (value == "yes") {
    $("#2-structurechange-table").css({ display: "flex" });
    structurechange_row++;
  } else {
    $("#2-structurechange-table").css({ display: "none" });
    structurechange_row=0;
  }
});

$("#2-structurechange-btn").on("click", function () {
  $(".2-square-inner").css({ display: "block", "padding-bottom": "80%" });
  $("#2-structurechange-images").css({ display: "flex" });
  $("#2-structurechange-btn").css({ display: "none" });
  $("#2-structurechange-btn2").css({ display: "block" });
});

$("#3-environmentchange").change(function () {
  var value = $(this).val();
  if (value == "yes") {
    $("#3-environmentchange-table").css({ display: "flex" });
    environmentchange=3;
  } else {
    $("#3-environmentchange-table").css({ display: "none" });
    environmentchange=0;
  }
});

$("#3-environmentchange-btn").on("click", function () {
  $(".3-square-inner").css({ display: "block", "padding-bottom": "80%" });
  $("#3-environmentchange-images").css({ display: "flex" });
  $("#3-environmentchange-btn").css({ display: "none" });
  $("#3-environmentchange-btn2").css({ display: "block" });
});

$("#4-expansion").change(function () {
  var value = $(this).val();
  if (value == "yes") {
    $("#4-expansion-table").css({ display: "flex" });
    expansion_row++;
  } else {
    $("#4-expansion-table").css({ display: "none" });
    expansion_row=0;
  }
});

$("#4-expansion-btn").on("click", function () {
  $(".4-square-inner").css({ display: "block", "padding-bottom": "80%" });
  $("#4-expansion-images").css({ display: "flex" });
  $("#4-expansion-btn").css({ display: "none" });
  $("#4-expansion-btn2").css({ display: "block" });
});

$("#5-overload").change(function () {
  var value = $(this).val();
  if (value == "yes") {
    $("#5-overload-table").css({ display: "flex" });
    overload++;
  } else {
    $("#5-overload-table").css({ display: "none" });
    overload=0;
  }
});

$("#5-overload-btn").on("click", function () {
  $(".5-square-inner").css({ display: "block", "padding-bottom": "80%" });
  $("#5-overload-images").css({ display: "flex" });
  $("#5-overload-btn").css({ display: "none" });
  $("#5-overload-btn2").css({ display: "block" });
});

$("#6-accident").change(function () {
  var value = $(this).val();
  if (value == "yes") {
    $("#6-accident-table").css({ display: "flex" });
    accident++;
  } else {
    $("#6-accident-table").css({ display: "none" });
    accident=0;
  }
});

$("#6-accident-btn").on("click", function () {
  $(".6-square-inner").css({ display: "block", "padding-bottom": "80%" });
  $("#6-accident-images").css({ display: "flex" });
  $("#6-accident-btn").css({ display: "none" });
  $("#6-accident-btn2").css({ display: "block" });
});

function dragOver(e) {
  e.stopPropagation();
  e.preventDefault();

  var bgvalue = $(e.target).css("background-color");

  // if ($(e.target).css("background-image")) {
  //   console.log("있다")
  // } else {
  //   console.log("없다")
  // }

  if (bgvalue === "rgb(167, 238, 250)") {
    // console.log(bgvalue);
  } else {
    if (e.type === "dragover") {
      $(e.target).css({ background: "rgb(167, 238, 255)" });
    } else {
      $(e.target).css({ background: "white" });
    }
  }
}

function uploadFiles(e) {
  var target_element = $(e.target);
  e.stopPropagation();
  e.preventDefault();
  if (e.originalEvent.dataTransfer.files.length > 1) {
    alert("하나만 올리세요");
    return;
  } else {
    imgFile = e.originalEvent.dataTransfer.files;
    imgFileName = imgFile[0].name;

    // 파일명 데이터에 추가
    var nametag = target_element.attr("name");
    console.log(nametag)
    fd.set(nametag, imgFileName);
 
    target_element.css({
      "background-image": "url(" + window.URL.createObjectURL(imgFile[0]) + ")",
      outline: "none",
      "background-size": "100%",
      "background-repeat": "no-repeat",
      "background-position": "center",
      "background-color":"rgb(167, 238, 250)"
    });
  }
}

$(".square")
  .on("dragover", dragOver)
  .on("dragleave", dragOver)
  .on("drop", uploadFiles);
