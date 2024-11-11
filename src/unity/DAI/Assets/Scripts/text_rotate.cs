using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class text_rotate : MonoBehaviour {
    private Camera _camera;
    void Start() {
        _camera = Camera.main;
    }
    void Update()
    {
        transform.LookAt(_camera.transform);
        transform.Rotate(0, 180, 0);
    }
}
