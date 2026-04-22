import boto3
import os
import time
from fastapi import HTTPException

class AthenaClient:
    def __init__(self):
        self.client = boto3.client(
            'athena',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
            region_name=os.getenv("AWS_REGION")
        )
        self.database = os.getenv("ATHENA_DATABASE")
        self.output_location = os.getenv("ATHENA_OUTPUT_LOCATION")

    async def execute_query(self, query: str):
        try:
            # Iniciar ejecución
            response = self.client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={'Database': self.database},
                ResultConfiguration={'OutputLocation': self.output_location}
            )
            query_execution_id = response['QueryExecutionId']

            # Esperar resultados (Polling)
            while True:
                status = self.client.get_query_execution(QueryExecutionId=query_execution_id)
                state = status['QueryExecution']['Status']['State']
                
                if state == 'SUCCEEDED':
                    break
                elif state in ['FAILED', 'CANCELLED']:
                    error_msg = status['QueryExecution']['Status'].get('StateChangeReason', 'Unknown error')
                    raise Exception(f"Athena query {state}: {error_msg}")
                
                time.sleep(1) # Esperar 1 segundo antes de reintentar

            # Obtener resultados
            results = self.client.get_query_results(QueryExecutionId=query_execution_id)
            return self._parse_results(results)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en AWS Athena: {str(e)}")

    def _parse_results(self, results):
        rows = results['ResultSet']['Rows']
        if not rows:
            return []
            
        # El primer elemento son las cabeceras
        headers = [col.get('VarCharValue') for col in rows[0]['Data']]
        
        data = []
        for row in rows[1:]:
            row_data = {}
            for i, col in enumerate(row['Data']):
                row_data[headers[i]] = col.get('VarCharValue')
            data.append(row_data)
            
        return data
