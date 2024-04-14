// Handles Upload of Images to S3 via API Gateway
// Converting to Base64 since direct upload was resulting in 0B images on S3
function uploadImage() {
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

  getBase64(file).then((data) => {
    var apigClient = apigClientFactory.newClient();
    var body = data;
    var customLabels = document.getElementById("CustomLabels").value;
    console.log(customLabels);
    var params = {
      // Change key to Filename
      filename: fileName + "_" + Date.now().toString(),
      // Change Bucket Name
      bucket: "cloudasst3-b2",
      "x-amz-meta-customLabels": customLabels,
    };

    // Change Function Call
    apigClient
      .uploadBucketFilenamePut(params, body, {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "*",
      })
      .then(function (res) {
        if (res.status == 200) {
          console.log("Uploaded successfully");
          alert("The Image was Uplaoded to S3!");
          console.log(res);
        }
      })
      .catch((err) => {
        console.log("Upload failed");
        console.log(err);
      });
  });
}

// Converts Image to Base64 encoded string
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

// Search Function to retrieve images
function searchText() {
  var searchTerm = document.getElementById("searchText").value;
  console.log(searchTerm);
  var apigClient = apigClientFactory.newClient();
  var params = {
    q: searchTerm,
  };
  var body = {};
  var additionalParams = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
  };
  apigClient
    .searchGet(params, body, additionalParams)
    .then(function (res) {
      console.log("success");
      console.log(res.data.images);
      showImages(res.data.images);
    })
    .catch(function (err) {
      console.log("Search Failed");
      console.log(err);
    });
}

// Decode Base64 Images and display to User
function showImages(images) {
  const searchResultDiv = document.getElementById("searchResult");
  searchResultDiv.innerHTML = "";
  console.log("Getting Here!");
  if (images.length === 0) {
    searchResultDiv.innerHTML = "No images found.";
  } else {
    images.forEach((imageb64) => {
      const img = document.createElement("img");
      // Convert From Base 64 to Image Format Again
      img.src = `data:image/jpeg;base64,${imageb64}`;
      img.style.width = "200px";
      img.style.margin = "5px";
      searchResultDiv.appendChild(img);
    });
  }
}
