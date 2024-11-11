using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.Serialization;
using UnityEngine.UI;

public class video_player : MonoBehaviour {
    public GameObject cubeGameObject;
    private cube _cube;
    public Scrollbar scrollbar;

    private bool _isPlaying = false;
    private Coroutine _loopCoroutine;
    public Button playPauseButton;
    private TextMeshProUGUI _playPauseButtonText;

    [FormerlySerializedAs("ValueTextGameObject")] public GameObject valueTextGameObject;
    private TextMeshProUGUI _valueText;
    
    void Start() {
        _cube = cubeGameObject.GetComponent<cube>();
        scrollbar.onValueChanged.AddListener(OnScrollbarValueChanged);
        _playPauseButtonText = playPauseButton.GetComponentInChildren<TextMeshProUGUI>();
        _valueText = valueTextGameObject.GetComponent<TextMeshProUGUI>();
    }

    private void Update() {
        if (_cube.SeqIdx > 0) _valueText.text = _cube.Sequence[_cube.SeqIdx - 1][6].ToString();
    }

    private void OnScrollbarValueChanged(float value) {
        int idxmax = _cube.Sequence.Count;
        int idx = Mathf.RoundToInt(value * idxmax);
        while (_cube.SeqIdx != idx) {
            if (_cube.SeqIdx > idx) _cube.PrevSeq();
            else _cube.NextSeq();
        }
    }

    public void IdxChanged() {
        int idxmax = _cube.Sequence.Count;
        float value = (float)_cube.SeqIdx / idxmax;
        scrollbar.onValueChanged.RemoveAllListeners();
        scrollbar.value = value;
        scrollbar.onValueChanged.AddListener(OnScrollbarValueChanged);
    }

    public void PlayPauseToggle() {
        if (_isPlaying) {
            PauseLoop();
        }
        else {
            StartLoop();
        }
    }
    
    private void StartLoop() {
        _isPlaying = true;
        _loopCoroutine = StartCoroutine(RunLoop());
        _playPauseButtonText.text = "Pause";
    }
    private void PauseLoop() {
        _isPlaying = false;
        if (_loopCoroutine != null) {
            StopCoroutine(_loopCoroutine);
        }
        _playPauseButtonText.text = "Play";
    }
    
    private IEnumerator RunLoop() {
        while (_cube.SeqIdx < _cube.Sequence.Count) {
            _cube.NextSeq();
            IdxChanged();
            yield return new WaitForSeconds((float)5/_cube.Sequence.Count);
        }
        if (_cube.SeqIdx == _cube.Sequence.Count) PauseLoop();
    }
}
