using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Serialization;

public class rotate : MonoBehaviour {
    [SerializeField] private Camera cam;
    private Vector3 _prevPos;
    public int rotatingSpeed = 10000;
    public int defaultRotate = 50;
    private Quaternion _defaultRotation;
    private float _threshold;

    void Start() {
        _defaultRotation = transform.rotation;
        _threshold = Screen.height * 0.8f;
    }
    void Update() {
        if (Input.mousePosition.y < _threshold) {
            if (Input.GetMouseButtonDown(0)) {
                _prevPos = cam.ScreenToViewportPoint(Input.mousePosition);
            }
            if (Input.GetMouseButton(0)) {
                Vector3 direction = (_prevPos - cam.ScreenToViewportPoint(Input.mousePosition)) * rotatingSpeed;
                float dirx = -direction.y;
                float diry = direction.x;
                if (Mathf.Abs(diry) > Mathf.Abs(dirx)) transform.Rotate(new Vector3(0, diry, 0) * Time.deltaTime, Space.World);
                else transform.Rotate(new Vector3(dirx, 0, 0) * Time.deltaTime, Space.World);
                _prevPos = cam.ScreenToViewportPoint(Input.mousePosition);
            }
        }
        if (Input.GetMouseButtonUp(0)) { 
            Vector3 current = transform.rotation.eulerAngles;
            current.x = Mathf.Round(current.x / 90f) * 90f;
            current.y = Mathf.Round(current.y / 90f) * 90f; 
            current.z = Mathf.Round(current.z / 90f) * 90f;
            _defaultRotation = Quaternion.Euler(current);
        }

        if (!Input.GetMouseButton(0)) {
            transform.rotation =
                Quaternion.RotateTowards(transform.rotation, _defaultRotation, defaultRotate * Time.deltaTime);
        }
    }
}
