#!/usr/bin/env python3
"""Helpers for quiet TensorFlow startup in interactive entry points."""

from __future__ import annotations

from contextlib import contextmanager
import os
import sys


def configure_tensorflow_env():
    """Set TensorFlow env vars before the first TensorFlow import."""
    os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"
    # Hide TensorFlow C++ INFO/WARNING startup logs.
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


# Apply the env configuration as soon as this module is imported so any
# subsequent TensorFlow import in this process sees the intended settings.
configure_tensorflow_env()


@contextmanager
def _suppress_stderr_fd():
    """Temporarily redirect process stderr to hide native startup noise."""
    stderr_fd = sys.stderr.fileno()
    saved_stderr_fd = os.dup(stderr_fd)
    try:
        with open(os.devnull, "w", encoding="utf-8") as devnull:
            os.dup2(devnull.fileno(), stderr_fd)
            yield
    finally:
        os.dup2(saved_stderr_fd, stderr_fd)
        os.close(saved_stderr_fd)


def configure_tensorflow_logging(tf):
    """Reduce Python-side TensorFlow and Abseil logging to errors only."""
    tf.get_logger().setLevel("ERROR")
    try:
        from absl import logging as absl_logging
    except ImportError:
        return

    absl_logging.set_verbosity(absl_logging.ERROR)
    absl_logging.set_stderrthreshold("error")


def import_tensorflow():
    """Import TensorFlow after applying startup log suppression."""
    if "tensorflow" in sys.modules:
        tf = sys.modules["tensorflow"]
        configure_tensorflow_logging(tf)
        return tf

    with _suppress_stderr_fd():
        import tensorflow as tf

    configure_tensorflow_logging(tf)
    return tf
