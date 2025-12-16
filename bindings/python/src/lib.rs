use pyo3::prelude::*;
use secure_protocol::{SecureContext, Config, SessionHandle};

/// Python wrapper for Config
#[pyclass]
#[derive(Clone)]
pub struct PyConfig {
    inner: Config,
}

#[pymethods]
impl PyConfig {
    #[new]
    #[pyo3(signature = (enable_forward_secrecy=true, enable_post_compromise_security=true))]
    fn new(enable_forward_secrecy: bool, enable_post_compromise_security: bool) -> Self {
        let mut cfg = Config::default();
        cfg.enable_forward_secrecy = enable_forward_secrecy;
        cfg.enable_post_compromise_security = enable_post_compromise_security;
        PyConfig { inner: cfg }
    }
}

/// Python wrapper for SecureContext
#[pyclass]
pub struct PySecureContext {
    inner: SecureContext,
}

#[pymethods]
impl PySecureContext {
    #[new]
    fn new(config: Option<PyConfig>) -> PyResult<Self> {
        let cfg = config.map(|c| c.inner).unwrap_or_default();
        let ctx = SecureContext::new(cfg).map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", e)))?;
        Ok(PySecureContext { inner: ctx })
    }

    fn create_session(&self, peer_id: &[u8]) -> PyResult<PySessionHandle> {
        let handle = self.inner.create_session(peer_id).map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", e)))?;
        Ok(PySessionHandle { inner: handle }) 
    }

    fn load_identity(&mut self, public: &[u8], private: &[u8]) {
        self.inner.load_identity(public, private);
    }
    
    fn encrypt_message(&self, session_id: &[u8], plaintext: &[u8]) -> PyResult<Vec<u8>> {
        self.inner.encrypt_message(session_id, plaintext, None)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", e)))
    }
    
    fn decrypt_message(&self, session_id: &[u8], ciphertext: &[u8]) -> PyResult<Vec<u8>> {
        self.inner.decrypt_message(session_id, ciphertext, None)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{}", e)))
    }
}

/// Session Handle wrapper
#[pyclass]
pub struct PySessionHandle {
    inner: SessionHandle,
}

#[pymethods]
impl PySessionHandle {
    fn peer_id(&self) -> Vec<u8> {
        self.inner.peer_id().to_vec()
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn _secure_protocol(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyConfig>()?;
    m.add_class::<PySecureContext>()?;
    m.add_class::<PySessionHandle>()?;
    Ok(())
}
