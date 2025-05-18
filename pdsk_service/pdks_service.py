import socket
import time

import servicemanager
import win32event
import win32service
import win32serviceutil

from pdsk_service.app import run_app


class PDKSService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PDKSSyncService"
    _svc_display_name_ = "Personel Devam Kontrol Sistemi Senkronizasyon Servisi"
    _svc_description_ = "PDSC cihazındaki kullanıcıları Oracle veritabanına senkronize eder."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True
        socket.setdefaulttimeout(60)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ""))
        self.main()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.running = False

    def main(self):
        while self.running:
            try:
                run_app()
                time.sleep(3600)  # Her 1 saatte bir çalıştır
            except Exception as e:
                servicemanager.LogMsg(servicemanager.EVENTLOG_ERROR_TYPE,
                                      servicemanager.PYS_SERVICE_EXCEPTION,
                                      (self._svc_name_, str(e)))
                time.sleep(60)


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PDKSService)
