import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://34.227.92.235:8100/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"max_stats"}>
					<tbody>
						<tr>
							<th>Sale of Item</th>
							<th>Number of Sales</th>
						</tr>
						<tr>
							<td># times bought before: {stats['max_num_times_bought_before']}</td>
							<td># vans needed: {stats['max_num_vans_needed']}</td>
						</tr>
						<tr>
							<td colspan="2">Max number of times bought before: {stats['max_num_times_bought_before']}</td>
						</tr>
						<tr>
							<td colspan="2">Max number of vans needed: {stats['max_num_vans_needed']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}
