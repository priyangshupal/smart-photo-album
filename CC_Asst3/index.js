const GET_API_ENDPOINT =
  "https://qe87xqnva5.execute-api.us-east-1.amazonaws.com/DEV";
const UPLOAD_API_ENDPOINT =
  "https://qe87xqnva5.execute-api.us-east-1.amazonaws.com/DEV/upload/cloudasst3-b2/";

function uploadImage() {
  console.log("Here!");
  var apigClient = apigClientFactory.newClient();
  const fileInput = document.getElementById("imageInput");
  const file = fileInput.files[0];
  const fileName = file.name;
  const fileType = file.type;
  if (!file) {
    alert("Please select an image file.");
    return;
  }

  const formData = new FormData();
  formData.append("image", file);

  console.log(fileName);
  console.log(fileType);

  getBase64(file).then((data) => {
    var apigClient = apigClientFactory.newClient();
    var fileType = file.type + ";base64";
    console.log(fileType);
    var body = data;
    var customLabels = "Dogs";
    var params = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "*",
      "Access-Control-Allow-Methods": "*",
      filename: Date.now().toString() + fileName,
      bucket: "cloudasst3-b2",
      "x-amz-meta-customLabels": customLabels,
    };
    console.log(params);
    apigClient
      .uploadBucketFilenamePut(params, body, {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "*",
        "x-amz-meta-customLabels": customLabels,
      })
      .then(function (res) {
        if (res.status == 200) {
          console.log("Uploaded successfully");
          console.log(res);
        }
      })
      .catch((err) => {
        console.log("Upload failed");
        console.log(err);
      });
  });
}

function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      let encoded = reader.result.replace(/^data:(.*;base64,)?/, "");
      if (encoded.length % 4 > 0) {
        encoded += "=".repeat(4 - (encoded.length % 4));
      }
      resolve(encoded);
    };
    reader.onerror = (error) => reject(error);
  });
}

function searchText() {
  var searchTerm = document.getElementById("searchText").value;
  console.log(searchTerm);
  var apigClient = apigClientFactory.newClient();
  var params = {
    "Access-Control-Allow-Origin": "*",
    q: searchTerm,
  };
  apigClient
    .searchGet(
      params,
      {},
      { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" }
    )
    .then(function (res) {
      console.log("success");
      console.log(res.data.images);
      showImages(res.data.images);
    })
    .catch(function (result) {
      console.log(result);
      console.log("NO RESULT");
    });
}

function showImages(images) {
  const searchResultDiv = document.getElementById("searchResult");
  searchResultDiv.innerHTML = "";
  console.log("Getting Here!");
  if (images.length === 0) {
    searchResultDiv.innerHTML = "No images found.";
  } else {
    images.forEach((imageb64) => {
      console.log("Reaching Here"); // Accessing each element of the array
      const img = document.createElement("img");
      img.src = `data:image/jpeg;base64,${imageb64}`;
      img.style.width = "200px";
      img.style.margin = "5px";
      searchResultDiv.appendChild(img);
    });
  }
}
