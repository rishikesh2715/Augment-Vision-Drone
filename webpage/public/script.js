import * as THREE from "three";
import { ThreeMFLoader } from "three/addons/loaders/3MFLoader.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
const renderer = new THREE.WebGLRenderer();
renderer.setClearColor(0x2d3142); // Set background color to white
renderer.setSize(window.innerWidth / 2, window.innerHeight);
document.getElementById("3d-container").appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.update();

const loader = new ThreeMFLoader();
loader.load("./droneV2.3mf", (object) => {
  object.scale.set(0.02, 0.02, 0.02); // Adjust the scale as needed
  object.rotation.x = (3 / 2) * Math.PI;
  scene.add(object);
  // Set camera position and look at the center of the scene
  camera.lookAt(0, 0, 0);

  const ambientLight = new THREE.AmbientLight(0xffffff); // Set ambient light color
  ambientLight.intensity = 0.5;
  scene.add(ambientLight);

  // // Create a directional light for overall illumination
  // const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
  // directionalLight.position.set(1, 1, 1).normalize();
  // scene.add(directionalLight);

  // Create a point light and attach it to the camera
  const pointLight = new THREE.PointLight(0xffffff, 25); // Adjust intensity
  camera.add(pointLight);
  pointLight.position.set(0, 0, 2);
  scene.add(camera);

  const keyframes = [
    // Define keyframes for position and rotation
    { position: { x: 0, y: 0, z: 0 }, rotation: { x: 4.8, z: 0 } },
    { position: { x: 2, y: -1, z: -2 }, rotation: { x: 6, z: 0.5 } },
    { position: { x: 4, y: -1, z: -2 }, rotation: { x: 6, z: 0 } },
    { position: { x: 2, y: -1, z: -2 }, rotation: { x: 6, z: -0.5 } },
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
});

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
