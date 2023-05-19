let navcount = 1;
let formData = new FormData();

$("#save").on("click", (e) => {
  const answer = confirm("글을 저장하시겠습니까?");

  // piccount를 pagecount로 변경할것
  formData.append("piccount", navcount.toString());
  formData.append("pagecount", navcount.toString());

  for (let i = 1; i <= 6 * navcount; i++) {
    const key = "picture-" + i.toString() + "-content";
    const value = $('input[name="input-' + i.toString() + '"]').val();

    formData.append(key, value);
  }

  // 아약스 전송
  $.ajax({
    url: "/picture/",
    data: formData,
    processData: false,
    contentType: false,
    method: "POST",
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

  if (answer) {
    alert("글을 저장하였습니다.");
  }
});

// 탭 추가
$("#nav-add").on("click", () => {
  if (navcount >= 3) {
    alert("현재 버전은 3페이지(사진 18장) 까지만 지원합니다.");
  } else {
    navcount++;
    
    $(".material-symbols-rounded").css({display:"none"});

    $("#nav-add-position").append(
      '<li class="nav-item"><a class="nav-link" id="nav-btn-' +
        navcount.toString() + '">' + '<span class="nav-inner">'+navcount.toString() + 
        '페이지</span>'+
        '<span class="material-symbols-rounded">backspace </span>'+
        '</a></li>'
    );
  }
});

// 탭 삭제
$("#nav-add-position").on("click", ".material-symbols-rounded" ,(e) => {
  const ask = confirm("해당 페이지의 사진이 모두 삭제됩니다. 현재 페이지를 삭제하시겠습니까?")
  if (ask) {
    $(".material-symbols-rounded").css({display:"flex"});
    $(e.target).parent().parent().remove(".nav-item");
    $("#page-" + navcount.toString()).css({ display: "none" });
    navcount--;
    for (let i = 1; i <= navcount; i++) {
      if (i === navcount) {
        $("#page-" + i.toString()).css({ display: "flex" });
        $("#nav-btn-" + i.toString()).attr("class", "nav-link active");
        $("#nav-btn-" + i.toString()).attr("aria-current", "page");
      } else {
        $("#page-" + i.toString()).css({ display: "none" });
        $("#nav-btn-" + i.toString()).attr("class", "nav-link");
        $("#nav-btn-" + i.toString()).attr("aria-current", "");
      }
    }
  }
})

// 탭을 클릭했을때
$("#nav-add-position").on("click", ".nav-inner", (e) => {
  const navbtnid = $(e.target).parent().attr("id");
  $(e.target).parent().attr("class", "nav-link active");
  $(e.target).parent().attr("aria-current", "page");
  const navbtnnum = navbtnid.split("-")[2];
  for (let i = 1; i <= navcount; i++) {
    if (i.toString() === navbtnnum) {
      $("#page-" + i.toString()).css({ display: "flex" });
    } else {
      $("#page-" + i.toString()).css({ display: "none" });
      $("#nav-btn-" + i.toString()).attr("class", "nav-link");
      $("#nav-btn-" + i.toString()).attr("aria-current", "");
    }
  }
});

function dragOver(e) {
  e.stopPropagation();
  e.preventDefault();

  var bgvalue = $(e.target).css("background-color");

  // 무조건 있다로 나옴;;
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
    var imgFile = e.originalEvent.dataTransfer.files;
    var imgFileName = imgFile[0].name;
    // console.log(imgFile[0]);
    target_element.html("");
    var nametag = target_element.attr("name");

    // 파일명 데이터에 추가
    formData.set(nametag, imgFileName);

    // 파일명 하단 input에 추가
    var inputtag = "input-" + nametag.split("-")[1];
    $("input[name=" + inputtag + "]").attr("value", imgFileName);
    // console.log($("input[name=" + inputtag + "]").val());

    target_element.css({
      "background-image": "url(" + window.URL.createObjectURL(imgFile[0]) + ")",
      outline: "none",
      padding: "35% 30%",
      "background-size": "100%",
      "background-repeat": "no-repeat",
      "background-position": "center",
      "background-color": "rgb(167, 238, 250)",
    });
  }
}

$(".square")
  .on("dragover", dragOver)
  .on("dragleave", dragOver)
  .on("drop", uploadFiles);
