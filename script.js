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
  console.log(object.children);
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
  const initialCameraPosition = { x: 0, y: 0, z: 5 };

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
    const progress =
      (window.scrollY -
        (currentKeyframe / (keyframes.length - 1)) *
          (document.documentElement.scrollHeight - window.innerHeight)) /
      ((nextKeyframe / (keyframes.length - 1)) *
        (document.documentElement.scrollHeight - window.innerHeight) -
        (currentKeyframe / (keyframes.length - 1)) *
          (document.documentElement.scrollHeight - window.innerHeight));

    console.log(nextKeyframe);
    console.log(progress);

    // Interpolate position
    const position = {
      x: THREE.MathUtils.lerp(
        keyframes[currentKeyframe].position.x,
        keyframes[nextKeyframe].position.x,
        progress
      ),
      y: THREE.MathUtils.lerp(
        keyframes[currentKeyframe].position.y,
        keyframes[nextKeyframe].position.y,
        progress
      ),
      z: THREE.MathUtils.lerp(
        keyframes[currentKeyframe].position.z,
        keyframes[nextKeyframe].position.z,
        progress
      ),
    };

    // Interpolate rotation
    const rotation = {
      x: THREE.MathUtils.lerp(
        keyframes[currentKeyframe].rotation.x,
        keyframes[nextKeyframe].rotation.x,
        progress
      ),
      z: THREE.MathUtils.lerp(
        keyframes[currentKeyframe].rotation.z,
        keyframes[nextKeyframe].rotation.z,
        progress
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
