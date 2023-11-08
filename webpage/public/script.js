import * as THREE from "three";
import { ThreeMFLoader } from "three/addons/loaders/3MFLoader.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  (window.innerWidth * 0.4) / (window.innerWidth * 0.4),
  0.1,
  1000
);
const renderer = new THREE.WebGLRenderer();
renderer.setClearColor(0x403f4c, 0); // Set background color to white
renderer.setSize(window.innerWidth * 0.4, window.innerWidth * 0.4);
renderer.setPixelRatio(window.devicePixelRatio);
document.getElementById("3d-container").appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.update();

const loader = new ThreeMFLoader();

// Before loading the model
document.getElementById("3d-container").style.display = "none";
document.getElementById("placeholderImage").style.opacity = "1";

loader.load("./droneV3extended.3mf", (object) => {
  let colors = [];

  object.traverse((child) => {
    if (child.material && child.material.color) {
      colors.push(child.material.color);
    }
  });

  object.scale.set(0.014, 0.014, 0.014); // Adjust the scale as needed
  object.rotation.x = (3 / 2) * Math.PI;
  scene.add(object);
  // Set camera position and look at the center of the scene
  camera.lookAt(0, 0, 0);

  const ambientLight = new THREE.AmbientLight(0xffffff); // Set ambient light color
  ambientLight.intensity = 0.5;
  scene.add(ambientLight);

  // Create a point light and attach it to the camera
  const pointLight = new THREE.PointLight(0xffffff, 25); // Adjust intensity
  camera.add(pointLight);
  pointLight.position.set(0, 0, 2);
  scene.add(camera);

  // At this point, your 3D model is set up and ready to be rendered
  // so, hide the placeholder image and show the 3D container
  document.getElementById("placeholderImage").style.opacity = "0";
  document.getElementById("3d-container").style.display = "block";

  setTimeout(() => {
    document.getElementById("placeholderImage").style.display = "none";
  }, 500); // Assuming you're using a 500ms fade-out for the image

  const keyframes = [
    // Define keyframes for position and rotation
    { position: { x: 0, y: 0, z: 0 }, rotation: { x: 4.8, z: 0 } },
    { position: { x: 1.25, y: -1, z: -2 }, rotation: { x: 6, z: 0.5 } },
    { position: { x: 2.5, y: -1, z: -2 }, rotation: { x: 6, z: 0 } },
    { position: { x: 1.25, y: -1, z: -2 }, rotation: { x: 6, z: -0.5 } },
    { position: { x: 0, y: -1, z: -2 }, rotation: { x: 6, z: 0 } },
    // Add more keyframes as needed
  ];

  // Current keyframe index
  let currentKeyframe = 0;

  // Initial camera position
  let initialCameraPosition;
  // Check the screen width to determine the initial camera position
  if (window.innerWidth <= 768) {
    // Set camera position for smaller screens
    initialCameraPosition = { x: 0, y: 0, z: 8 };
  } else {
    // Set camera position for larger screens
    initialCameraPosition = { x: 0, y: 0, z: 4 };
  }

  // Set the initial camera position
  camera.position.set(
    initialCameraPosition.x,
    initialCameraPosition.y,
    initialCameraPosition.z
  );

  const animate = () => {
    requestAnimationFrame(animate);
    // Interpolate between keyframes
    const nextKeyframe = (currentKeyframe + 1) % keyframes.length;
    let totalY = document.documentElement.scrollHeight - window.innerHeight;
    let currentY = window.scrollY;
    let currentStepStartY = (currentKeyframe / (keyframes.length - 1)) * totalY;
    let nextStepStartY = (nextKeyframe / (keyframes.length - 1)) * totalY;
    const progressCurrentStep =
      (currentY - currentStepStartY) / (nextStepStartY - currentStepStartY);

    // Interpolate position
    const position = {
      x: THREE.MathUtils.lerp(
        keyframes[currentKeyframe].position.x,
        keyframes[nextKeyframe].position.x,
        progressCurrentStep
      ),
      y: THREE.MathUtils.lerp(
        keyframes[currentKeyframe].position.y,
        keyframes[nextKeyframe].position.y,
        progressCurrentStep
      ),
      z: THREE.MathUtils.lerp(
        keyframes[currentKeyframe].position.z,
        keyframes[nextKeyframe].position.z,
        progressCurrentStep
      ),
    };

    // Interpolate rotation
    const rotation = {
      x: THREE.MathUtils.lerp(
        keyframes[currentKeyframe].rotation.x,
        keyframes[nextKeyframe].rotation.x,
        progressCurrentStep
      ),
      z: THREE.MathUtils.lerp(
        keyframes[currentKeyframe].rotation.z,
        keyframes[nextKeyframe].rotation.z,
        progressCurrentStep
      ),
    };

    // Set the object's position and rotation
    object.position.set(position.x, position.y, position.z);
    object.rotation.set(rotation.x, 0, rotation.z);

    renderer.render(scene, camera);
    // Assuming you're using a PerspectiveCamera
    window.addEventListener("resize", () => {
      let newWidth = window.innerWidth;
      let newHeight = window.innerHeight;

      // If the window width is 768px or less
      if (newWidth <= 768) {
        newWidth = newWidth * 0.92; // 92% of the view width
        newHeight = newWidth; // Keep it square since you mentioned 92% of the view width
        object.scale.set(0.028, 0.028, 0.028); // Adjust the scale as needed
      } else {
        newWidth = newWidth * 0.4; // 92% of the view width
        newHeight = newWidth; // Keep it square since you mentioned 92% of the view width
        object.scale.set(0.014, 0.014, 0.014); // Adjust the scale as needed
      }

      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();

      renderer.setSize(newWidth, newHeight);
    });

    window.dispatchEvent(new Event("resize"));
  };

  animate();

  window.addEventListener("scroll", () => {
    // Set the initial camera position
    camera.position.set(
      initialCameraPosition.x,
      initialCameraPosition.y,
      initialCameraPosition.z
    );
    camera.lookAt(0, 0, 0);
    requestAnimationFrame(() => {
      // Calculate the scroll position as a percentage of the total scrollable area
      const scrollPercentage =
        window.scrollY /
        (document.documentElement.scrollHeight - window.innerHeight);

      // Calculate the new keyframe based on the scroll percentage
      const newKeyframe = Math.floor(scrollPercentage * (keyframes.length - 1));

      if (newKeyframe !== currentKeyframe) {
        currentKeyframe = newKeyframe;
      }
    });
  });
  // captureAndSaveSnapshot();
});

function captureAndSaveSnapshot() {
  // Make sure to render the scene first
  renderer.render(scene, camera);

  // Extract the image data
  const imgData = renderer.domElement.toDataURL("image/png");

  // Create a link element
  const link = document.createElement("a");
  link.href = imgData;
  link.download = "snapshot.png";

  // Trigger a click on the link to start the download
  link.click();
}

// V1 3d Model

const sceneV1 = new THREE.Scene();
const cameraV1 = new THREE.PerspectiveCamera(
  75,
  (window.innerWidth * 0.4) / (window.innerWidth * 0.4),
  0.1,
  1000
);
cameraV1.position.set(0, 0, 2.5); // Adjust these values to position the camera

const rendererV1 = new THREE.WebGLRenderer();
rendererV1.setClearColor(0xabcdef, 0); // Sets a light blue color for clarity
rendererV1.setSize(window.innerWidth * 0.4, window.innerWidth * 0.4);

document
  .getElementById("version1threeDcontainer")
  .appendChild(rendererV1.domElement);

const controlsV1 = new OrbitControls(cameraV1, rendererV1.domElement);
controlsV1.update();

const loaderV1 = new ThreeMFLoader();

loaderV1.load("./droneVone.3mf", (objectV1) => {
  objectV1.scale.set(0.01, 0.01, 0.01); // Adjust these values as needed
  objectV1.rotation.x = (3 / 2) * Math.PI;

  sceneV1.add(objectV1);

  const ambientLight = new THREE.AmbientLight(0xffffff); // Set ambient light color
  ambientLight.intensity = 0.5;
  sceneV1.add(ambientLight);

  // Create a point light and attach it to the camera
  const pointLight = new THREE.PointLight(0xffffff, 25); // Adjust intensity
  cameraV1.add(pointLight);
  pointLight.position.set(0, 0, 2);
  sceneV1.add(cameraV1);

  const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1);
  light.position.set(0, 1, 0);
  sceneV1.add(light);
});

const animateV1 = () => {
  requestAnimationFrame(animateV1);
  rendererV1.render(sceneV1, cameraV1);
};

animateV1();

// N&W 3d Model

const sceneNandW = new THREE.Scene();
const cameraNandW = new THREE.PerspectiveCamera(
  75,
  (window.innerWidth * 0.4) / (window.innerWidth * 0.4),
  0.1,
  1000
);
cameraNandW.position.set(0, 0, 2.5); // Adjust these values to position the camera

const rendererNandW = new THREE.WebGLRenderer();
rendererNandW.setClearColor(0xabcdef, 0); // Sets a light blue color for clarity
rendererNandW.setSize(window.innerWidth * 0.4, window.innerWidth * 0.4);

document
  .getElementById("NandW3Dcontainer")
  .appendChild(rendererNandW.domElement);

const controlsNandW = new OrbitControls(cameraNandW, rendererNandW.domElement);
controlsNandW.update();

const loaderNandW = new ThreeMFLoader();

loaderNandW.load("./droneV1.3mf", (objectNandW) => {
  objectNandW.scale.set(0.01, 0.01, 0.01); // Adjust these values as needed
  objectNandW.rotation.x = (3 / 2) * Math.PI;

  sceneNandW.add(objectNandW);

  const ambientLight = new THREE.AmbientLight(0xffffff); // Set ambient light color
  ambientLight.intensity = 0.5;
  sceneNandW.add(ambientLight);

  // Create a point light and attach it to the camera
  const pointLight = new THREE.PointLight(0xffffff, 25); // Adjust intensity
  cameraNandW.add(pointLight);
  pointLight.position.set(0, 0, 2);
  sceneNandW.add(cameraNandW);

  const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1);
  light.position.set(0, 1, 0);
  sceneNandW.add(light);
});

const animateNandW = () => {
  requestAnimationFrame(animateNandW);
  rendererNandW.render(sceneNandW, cameraNandW);
};

animateNandW();

// armLock 3d Model

const sceneArmLock = new THREE.Scene();
const cameraArmLock = new THREE.PerspectiveCamera(
  75,
  (window.innerWidth * 0.4) / (window.innerWidth * 0.4),
  0.1,
  1000
);
cameraArmLock.position.set(0, 0, 2.5); // Adjust these values to position the camera

const rendererArmLock = new THREE.WebGLRenderer();
rendererArmLock.setClearColor(0xabcdef, 0); // Sets a light blue color for clarity
rendererArmLock.setSize(window.innerWidth * 0.4, window.innerWidth * 0.4);

document
  .getElementById("armLock3Dcontainer")
  .appendChild(rendererArmLock.domElement);

const controlsArmLock = new OrbitControls(
  cameraArmLock,
  rendererArmLock.domElement
);
controlsArmLock.update();

const loaderArmLock = new ThreeMFLoader();

loaderArmLock.load("./droneV3extended.3mf", (objectArmLock) => {
  objectArmLock.scale.set(0.01, 0.01, 0.01); // Adjust these values as needed
  objectArmLock.rotation.x = (3 / 2) * Math.PI;

  sceneArmLock.add(objectArmLock);

  const ambientLight = new THREE.AmbientLight(0xffffff); // Set ambient light color
  ambientLight.intensity = 0.5;
  sceneArmLock.add(ambientLight);

  // Create a point light and attach it to the camera
  const pointLight = new THREE.PointLight(0xffffff, 25); // Adjust intensity
  cameraArmLock.add(pointLight);
  pointLight.position.set(0, 0, 2);
  sceneArmLock.add(cameraArmLock);

  const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1);
  light.position.set(0, 1, 0);
  sceneArmLock.add(light);
});

const animateArmLock = () => {
  requestAnimationFrame(animateArmLock);
  rendererArmLock.render(sceneArmLock, cameraArmLock);
};

animateArmLock();

document
  .getElementById("subscribe-button")
  .addEventListener("click", function () {
    const email = document.getElementById("newsletter-email").value;

    // Perform client-side validation here (e.g., check for a valid email format)
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    if (!emailRegex.test(email)) {
      alert("Invalid email format");
      return; // Exit the function early
    }

    // Send the email to the server for further processing
    fetch("/subscribe", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email }),
    })
      .then((response) => {
        if (response.ok) {
          // Display a success message to the user
          alert("Subscription successful! Check your email for confirmation.");
          document.getElementById("newsletter-email").value = "";
        } else {
          // Parse the JSON error response and display the error message
          response
            .json()
            .then((data) => {
              alert(`Subscription failed. ${data.error}`);
            })
            .catch((error) => {
              console.error("Error parsing JSON response:", error);
              alert("Subscription failed. An error occurred.");
            });
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

let version1Element = document.getElementById("version1");
let NandWelement = document.getElementById("NandW");
let armLockElement = document.getElementById("armLock");
let newsletterContentElement = document.getElementById("newsletterContent");

function getClassNames(elementId) {
  let baseName = elementId.charAt(0).toUpperCase() + elementId.slice(1);
  return {
    visibleClass: "visible" + baseName,
    hiddenClass: "hidden" + baseName,
  };
}

// Function to show a section
function showSection(storyElement, sectionID) {
  // Hide all sections
  hideAllSections();
  // Add visible class to the specified section
  let classNames = getClassNames(storyElement.id);
  storyElement.classList.remove(classNames.hiddenClass);
  storyElement.classList.add(classNames.visibleClass);

  // Remove newsletter content visible state
  newsletterContentElement.classList.remove("visibleNewsletter");
  newsletterContentElement.classList.add("hiddenNewsletter");

  // Set the background for the active section
  if (sectionID) {
    document.getElementById(sectionID).style.backgroundImage =
      "linear-gradient(to left, rgba(20, 19, 25, 0.75), rgba(20, 19, 25, 0.95))";
  }

  // Display the section
  storyElement.style.display = "block";
}

// Function to hide a section
function hideSection(storyElement) {
  let classNames = getClassNames(storyElement.id);
  // Remove visible state and add hidden class
  storyElement.classList.remove(classNames.visibleClass);
  storyElement.classList.add(classNames.hiddenClass);

  let sectionID = storyElement.id + "section";
  document.getElementById(sectionID).style.backgroundImage =
    "linear-gradient(to left, rgba(20, 19, 25, 0.05), rgba(20, 19, 25, 0.95))";
}

// Hide all sections and show newsletter content by default
function hideAllSections() {
  [version1Element, NandWelement, armLockElement].forEach(hideSection);
}

// Set up animation end event listener to hide elements when their animation is complete
[
  version1Element,
  NandWelement,
  armLockElement,
  newsletterContentElement,
].forEach((mainElement) => {
  mainElement.addEventListener("animationend", function (event) {
    let reverseAnimationName =
      "reverse" +
      mainElement.id.charAt(0).toUpperCase() +
      mainElement.id.slice(1) +
      "animation";
    console.log(reverseAnimationName);
    if (event.animationName === reverseAnimationName) {
      mainElement.style.display = "none";

      if (event.animationName === "reverseNewsletterContentanimation") {
        document.getElementById("newsletterTitle").style.textDecoration =
          "underline";
        document.getElementById("newsletterTitle").style.cursor = "pointer";
      }
    }
  });
});

function showNewsletter() {
  // Ensure newsletter content has correct visibility state
  newsletterContentElement.classList.remove("hiddenNewsletter");
  newsletterContentElement.classList.add("visibleNewsletter");

  // Handle decoration and cursor for the newsletter title
  document.getElementById("newsletterTitle").style.textDecoration = "none";
  document.getElementById("newsletterTitle").style.cursor = "auto";
  newsletterContentElement.style.display = "flex";
}

// Click event listener for toggling visibility
document.addEventListener("click", function (eve) {
  // If the click is inside version1, NandW, or armLock, do nothing
  if (
    eve.target.closest("#version1") ||
    eve.target.closest("#NandW") ||
    eve.target.closest("#armLock")
  ) {
    return; // Exit the function early
  }

  const clickedSection = eve.target.closest(".section");

  // If a section was clicked, determine which one and make it active
  if (clickedSection) {
    switch (clickedSection.id) {
      case "version1section":
        showSection(version1Element, clickedSection.id);
        break;
      case "NandWsection":
        showSection(NandWelement, clickedSection.id);
        break;
      case "armLocksection":
        showSection(armLockElement, clickedSection.id);
        break;
      default:
        hideAllSections();
        break;
    }
  } else {
    // If clicked outside of sections, hide all and show newsletter content
    hideAllSections();
    showNewsletter();
  }
});

// Initialize the page with all sections hidden except newsletter content
hideAllSections();
