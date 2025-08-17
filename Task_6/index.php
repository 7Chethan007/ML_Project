<?php
include 'db.php';

$result = $conn->query("SELECT company_id, company_name FROM ml ORDER BY company_name ASC");
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Company Analysis - ML Project</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
  <style>
    body { background-color: #f8f9fa; }
    .card-custom { box-shadow: 0px 2px 6px rgba(0,0,0,0.1); }
  </style>
</head>
<body class="container mt-4">

  <h2 class="mb-4">Companies - ML Insights</h2>

  <div class="card card-custom p-3">
    <table class="table table-bordered table-striped">
      <thead class="table-dark">
        <tr>
          <th>Company ID</th>
          <th>Company Name</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <?php while($row = $result->fetch_assoc()): ?>
          <tr>
            <td><?= htmlspecialchars($row['company_id']) ?></td>
            <td><?= htmlspecialchars($row['company_name']) ?></td>
            <td>
              <a href="company.php?id=<?= urlencode($row['company_id']) ?>" class="btn btn-primary btn-sm">View Analysis</a>
            </td>
          </tr>
        <?php endwhile; ?>
      </tbody>
    </table>
  </div>

</body>
</html>
