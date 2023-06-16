let appendRowCount = 0;

$("#temporary").on("click", function () {
  let fd = new FormData();
  fd.append("usagechange-length",appendRowCount)
  for (let i = 1; i <= appendRowCount; i++) {
    for (let j = 1; j <= 7; j++) {
      fd.append(
        "usagechange-"+i.toString(),
        $("input[name=1-" + i.toString() + "-" + j.toString() + "]").val()
      );
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

$("#1-usagechange-appendrow-button").on("click", () => {
  appendRowCount++;
  $("#1-usagechange-appendrow").append(
    '<div class="row">' +
      '<div class="col"><input class="input-in-grid" name="1-' +
      appendRowCount.toString() +
      '-1"/></div>' +
      '<div class="col-4"><div class="container text-center"><div></div><div class="row">' +
      '<div class="col-8"><input class="input-in-grid" name="1-' +
      appendRowCount.toString() +
      '-2"/></div>' +
      '<div class="col"><input class="input-in-grid" name="1-' +
      appendRowCount.toString() +
      '-3"/></div>' +
      "</div></div></div>" +
      '<div class="col-4"><div class="container text-center"><div></div><div class="row">' +
      '<div class="col-8"><input class="input-in-grid" name="1-' +
      appendRowCount.toString() +
      '-4"/></div>' +
      '<div class="col"><input class="input-in-grid" name="1-' +
      appendRowCount.toString() +
      '-5"/></div>' +
      "</div></div></div>" +
      '<div class="col"><input class="input-in-grid" name="1-' +
      appendRowCount.toString() +
      '-6"/></div>' +
      '<div class="col"><input class="input-in-grid" name="1-' +
      appendRowCount.toString() +
      '-7"/></div>' +
      "</div>"
  );
  console.log(appendRowCount);
});

/* Checkbox change event */
$("#1-usagechange").change(function () {
  var value = $(this).val();
  if (value == "yes") {
    $("#1-usagechange-table").css({ display: "flex" });
    appendRowCount++;
  } else {
    $("#1-usagechange-table").css({ display: "none" });
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
  } else {
    $("#2-structurechange-table").css({ display: "none" });
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
  } else {
    $("#3-environmentchange-table").css({ display: "none" });
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
  } else {
    $("#4-expansion-table").css({ display: "none" });
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
  } else {
    $("#5-overload-table").css({ display: "none" });
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
  } else {
    $("#6-accident-table").css({ display: "none" });
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
  if (e.type === "dragover") {
    $(e.target).css({ background: "grey" });
  } else {
    $(e.target).css({ background: "white" });
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
    console.log(imgFile[0]);
    target_element.css({
      "background-image": "url(" + window.URL.createObjectURL(imgFile[0]) + ")",
      outline: "none",
      "background-size": "100%",
      "background-repeat": "no-repeat",
      "background-position": "center",
    });
  }
}

$(".square")
  .on("dragover", dragOver)
  .on("dragleave", dragOver)
  .on("drop", uploadFiles);
