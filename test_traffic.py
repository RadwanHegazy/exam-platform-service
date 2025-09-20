import json
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_headers(
    email='ahmed@gmail.com',
    password='ahmed'
): 
    req = requests.post(
        'http://localhost/users/auth/student/login/v1/',
        data={
            'email': email,
            'password': password
        }
    )
    tokens = req.json()['access']
    return {
        "Content-Type" : "application/json",
        'Authorization': f"Bearer {tokens}",
    }

def make_solver_request(request_id):
    """Make a single solver request"""
    try:
        req = requests.post(
            'http://localhost:80/solver',
            json={
                'exam_id': int(1),
                'question_id': int(1),
                'answer': "a"
            },
            headers=get_headers(),
            timeout=30  # Add timeout to prevent hanging,
        )
        
        # Check if status code is 201 for success
        success = req.ok

        print(req.json())
        
        return {
            'request_id': request_id,
            'status_code': req.status_code,
            'response': req.json() if success else {"error": f"Unexpected status code: {req.status_code}"},
            'success': success
        }
    except Exception as e:
        return {
            'request_id': request_id,
            'error': str(e),
            'success': False,
            'status_code': None
        }

def run_load_test(total_requests=1000, num_threads=10):
    """Run load test with multiple threads"""
    print(f"Starting load test: {total_requests} requests with {num_threads} threads")
    start_time = time.time()
    
    successful_requests = 0
    failed_requests = 0
    status_code_counts = {}  # Track frequency of each status code
    results = []
    
    # Use ThreadPoolExecutor for concurrent requests
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit all requests
        future_to_request = {
            executor.submit(make_solver_request, i): i 
            for i in range(total_requests)
        }
        
        # Process completed requests
        for future in as_completed(future_to_request):
            result = future.result()
            results.append(result)
            
            # Track status codes
            status_code = result.get('status_code')
            if status_code is not None:
                status_code_counts[status_code] = status_code_counts.get(status_code, 0) + 1
            
            # Check if request was successful (status code 201)
            if result['success']:
                successful_requests += 1
            else:
                failed_requests += 1
            
            # Print progress every 1000 requests
            if len(results) % 1000 == 0:
                print(f"Completed {len(results)}/{total_requests} requests...")
                print(f"  Success: {successful_requests}, Failed: {failed_requests}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Calculate metrics
    requests_per_second = total_requests / total_time if total_time > 0 else 0
    avg_time_per_request = total_time / total_requests if total_requests > 0 else 0
    
    print("\n" + "="*60)
    print("LOAD TEST RESULTS")
    print("="*60)
    print(f"Total requests: {total_requests}")
    print(f"Successful requests (201): {successful_requests}")
    print(f"Failed requests: {failed_requests}")
    print(f"Success rate: {(successful_requests/total_requests)*100:.2f}%")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Requests per second: {requests_per_second:.2f}")
    print(f"Average time per request: {avg_time_per_request:.4f} seconds")
    
    # Print status code distribution
    print("\nStatus code distribution:")
    for code, count in sorted(status_code_counts.items()):
        percentage = (count / total_requests) * 100
        print(f"  {code}: {count} requests ({percentage:.2f}%)")
    
    print("="*60)
    
    # Print some error samples if any failed
    if failed_requests > 0:
        print("\nSample errors:")
        error_samples = [r for r in results if not r['success']][:5]
        for i, error in enumerate(error_samples, 1):
            status_code_info = f", Status: {error['status_code']}" if error.get('status_code') else ""
            print(f"{i}. Request {error['request_id']}{status_code_info}: {error.get('error', 'Unknown error')}")
    
    return results, total_time

if __name__ == "__main__":
    # Warm up with a single request to check connectivity and expected status code
    print("Testing connectivity and expected response...")
    try:
        test_result = make_solver_request(0)
        if test_result['success']:
            print("✓ Connectivity test passed - Received status 201")
        else:
            print(f"✗ Connectivity test failed - Received status {test_result.get('status_code', 'Unknown')}")
            if test_result.get('error'):
                print(f"Error: {test_result['error']}")
            exit(1)
    except Exception as e:
        print(f"✗ Connectivity test failed: {e}")
        exit(1)
    
    # Run the load test
    print("\nStarting main load test...")
    results, total_time = run_load_test() 