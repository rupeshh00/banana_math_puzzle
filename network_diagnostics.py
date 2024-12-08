#!/usr/bin/env python3
"""
Banana Math Puzzle Network Diagnostics

Comprehensive network diagnostic tool to validate:
- Internet connectivity
- DNS resolution
- Local network status
- API endpoint availability
- Security and performance metrics
"""

import os
import sys
import asyncio
import socket
import ssl
import json
import time
import yaml
import platform
import subprocess
import speedtest
import aiohttp
import pytest
import logging
import requests
import ipaddress
import traceroute  # New library for advanced tracing
import dns.resolver  # For advanced DNS resolution checks
import certifi
import OpenSSL
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from functools import wraps

# Configuration and Core Imports
from src.game.core.config import load_config
from src.game.banana_api import banana_api, get_banana_api_key

# Load Network Diagnostics Configuration
def load_network_config():
    config_path = os.path.join(os.path.dirname(__file__), 'src', 'game', 'core', 'network_diagnostics_config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

NETWORK_CONFIG = load_network_config()

# Enhanced Logging Configuration
logging.basicConfig(
    level=getattr(logging, NETWORK_CONFIG['network_diagnostics']['logging']['level']),
    format='%(asctime)s | %(levelname)8s | %(module)15s | %(message)s',
    handlers=[
        logging.FileHandler(
            NETWORK_CONFIG['network_diagnostics']['logging']['file'], 
            maxBytes=NETWORK_CONFIG['network_diagnostics']['logging']['max_file_size_mb'] * 1024 * 1024,
            backupCount=NETWORK_CONFIG['network_diagnostics']['logging']['backup_count']
        ),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class HostDiagnosticResult:
    """Comprehensive host diagnostic result"""
    host: str
    ip: Optional[str] = None
    reachable: bool = False
    latency: float = 0.0
    error: Optional[str] = None
    ssl_info: Dict[str, Any] = field(default_factory=dict)
    dns_info: Dict[str, Any] = field(default_factory=dict)
    trace_route: List[str] = field(default_factory=list)

class EnhancedNetworkDiagnostics:
    """
    Advanced network diagnostics with comprehensive checks.
    """
    
    def __init__(self, config=None):
        """
        Initialize network diagnostics with optional configuration override.
        
        Args:
            config: Optional configuration dictionary to override defaults
        """
        self.config = config or NETWORK_CONFIG['network_diagnostics']
        self.timeout = self.config['timeout']
    
    def _resolve_dns(self, hostname: str) -> Dict[str, Any]:
        """
        Perform advanced DNS resolution with multiple record type checks.
        
        Args:
            hostname: Hostname to resolve
        
        Returns:
            Dictionary with DNS resolution details
        """
        dns_results = {
            'A': [],     # IPv4 records
            'AAAA': [],  # IPv6 records
            'MX': [],    # Mail exchange records
            'NS': []     # Name server records
        }
        
        try:
            for record_type in dns_results.keys():
                try:
                    answers = dns.resolver.resolve(hostname, record_type)
                    dns_results[record_type] = [str(rdata) for rdata in answers]
                except dns.resolver.NoAnswer:
                    pass  # No records of this type
                except Exception as e:
                    logger.warning(f"DNS resolution error for {hostname} ({record_type}): {e}")
        except Exception as e:
            logger.error(f"Comprehensive DNS resolution failed for {hostname}: {e}")
        
        return dns_results
    
    def _check_ssl_certificate(self, hostname: str) -> Dict[str, Any]:
        """
        Perform comprehensive SSL/TLS certificate check.
        
        Args:
            hostname: Hostname to check SSL certificate
        
        Returns:
            Dictionary with SSL certificate details
        """
        try:
            # Create SSL context
            context = ssl.create_default_context(cafile=certifi.where())
            
            with socket.create_connection((hostname, 443), timeout=self.timeout['ssl_check']) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                    # Get certificate
                    cert = secure_sock.getpeercert(binary_form=False)
                    x509 = OpenSSL.crypto.load_certificate(
                        OpenSSL.crypto.FILETYPE_ASN1, 
                        secure_sock.getpeercert(binary_form=True)
                    )
                    
                    # Extract certificate details
                    expiry_date = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
                    days_until_expiry = (expiry_date - datetime.now()).days
                    
                    return {
                        'valid': days_until_expiry > 0,
                        'days_until_expiry': days_until_expiry,
                        'issuer': dict(x509.get_issuer().get_components()),
                        'subject': dict(x509.get_subject().get_components()),
                        'version': x509.get_version(),
                        'serial_number': x509.get_serial_number(),
                        'protocols': secure_sock.version()
                    }
        except Exception as e:
            logger.error(f"SSL certificate check failed for {hostname}: {e}")
            return {
                'valid': False,
                'error': str(e)
            }
    
    def _trace_route(self, hostname: str) -> List[str]:
        """
        Perform trace route to the specified hostname.
        
        Args:
            hostname: Hostname to trace route
        
        Returns:
            List of IP addresses in the route
        """
        try:
            # Use traceroute library for cross-platform compatibility
            route = traceroute.traceroute(hostname)
            return [hop.ip for hop in route]
        except Exception as e:
            logger.error(f"Trace route failed for {hostname}: {e}")
            return []
    
    def comprehensive_host_check(self, host_config: Dict[str, Any]) -> HostDiagnosticResult:
        """
        Perform comprehensive diagnostic check for a host.
        
        Args:
            host_config: Host configuration dictionary
        
        Returns:
            Comprehensive host diagnostic result
        """
        hostname = host_config['url'].replace('https://', '').replace('http://', '')
        
        result = HostDiagnosticResult(host=hostname)
        
        try:
            # Resolve IP
            result.ip = socket.gethostbyname(hostname)
            
            # Connectivity check
            start_time = time.time()
            with socket.create_connection((result.ip, 443), timeout=self.timeout['connection']) as sock:
                result.reachable = True
                result.latency = (time.time() - start_time) * 1000  # ms
            
            # Advanced checks
            if self.config['advanced_features']['dns_resolution_check']:
                result.dns_info = self._resolve_dns(hostname)
            
            if self.config['advanced_features']['trace_route']:
                result.trace_route = self._trace_route(hostname)
            
            # SSL Certificate Check
            result.ssl_info = self._check_ssl_certificate(hostname)
        
        except Exception as e:
            result.reachable = False
            result.error = str(e)
            logger.error(f"Host check failed for {hostname}: {e}")
        
        return result
    
    def run_comprehensive_network_check(self) -> Dict[str, Any]:
        """
        Run comprehensive network diagnostics across configured hosts.
        
        Returns:
            Detailed network diagnostic results
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'host_checks': [],
            'performance_metrics': {},
            'overall_status': True
        }
        
        # Check primary and game-specific endpoints
        all_hosts = (
            self.config['hosts']['primary_endpoints'] + 
            self.config['hosts']['game_specific']
        )
        
        for host_config in all_hosts:
            host_result = self.comprehensive_host_check(host_config)
            results['host_checks'].append(asdict(host_result))
            results['overall_status'] &= host_result.reachable
        
        # Network Performance Test
        try:
            st = speedtest.Speedtest()
            download_speed = st.download() / 1_000_000  # Mbps
            upload_speed = st.upload() / 1_000_000  # Mbps
            
            results['performance_metrics'] = {
                'download_speed_mbps': round(download_speed, 2),
                'upload_speed_mbps': round(upload_speed, 2),
                'download_status': self._evaluate_speed(download_speed, 'download'),
                'upload_status': self._evaluate_speed(upload_speed, 'upload')
            }
        except Exception as e:
            logger.error(f"Performance test failed: {e}")
            results['performance_metrics'] = {
                'error': str(e)
            }
        
        return results
    
    def _evaluate_speed(self, speed: float, speed_type: str) -> str:
        """
        Evaluate network speed against configured thresholds.
        
        Args:
            speed: Measured speed in Mbps
            speed_type: 'download' or 'upload'
        
        Returns:
            Speed status: 'good', 'warning', or 'critical'
        """
        thresholds = self.config['performance_thresholds'][f'{speed_type}_speed_mbps']
        
        if speed >= thresholds['warning']:
            return 'good'
        elif speed >= thresholds['critical']:
            return 'warning'
        else:
            return 'critical'

def log_network_diagnostics():
    """Log comprehensive network diagnostics with structured output"""
    diagnostics = EnhancedNetworkDiagnostics()
    results = diagnostics.run_comprehensive_network_check()
    
    # Pretty print results
    logger.info("🌐 Network Diagnostic Results:")
    logger.info(json.dumps(results, indent=2))
    
    return results

# Optional: Run diagnostics on import
if __name__ == "__main__":
    log_network_diagnostics()
