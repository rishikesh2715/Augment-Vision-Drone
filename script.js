import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { FBXLoader } from "three/addons/loaders/FBXLoader.js";

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
const renderer = new THREE.WebGLRenderer();
renderer.setClearColor(0, 0, 0, 0);
renderer.setSize(window.innerWidth / 2, window.innerHeight);

document.getElementById("3dModel").appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.update();

const loader = new FBXLoader();

loader.load("./HotDog.fbx", (object) => {
  object.scale.set(0.25, 0.25, 0.25);
  object.rotation.y = (3 / 2) * Math.PI;
  scene.add(object);

  camera.lookAt(0, 0, 0);

  const ambientLight = new THREE.AmbientLight(0xffffff);
  ambientLight.intensity = 0.5;
  scene.add(ambientLight);

  const pointLight = new THREE.PointLight(0xffffff, 25);
  camera.add(pointLight);
  pointLight.position.set(0, 0, 2);
  scene.add(camera);

  const initialCameraPosition = { x: 0, y: 0, z: 5 };

  camera.position.set(
    initialCameraPosition.x,
    initialCameraPosition.y,
    initialCameraPosition.z
  );

  const animate = () => {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
  };

  animate();

  window.addEventListener("scroll", () => {
    object.rotation.x = window.scrollY;
  });
});
